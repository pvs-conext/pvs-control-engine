/*
 * Copyright 2017-present Open Networking Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.onosproject.p4tutorial.mytunnel;

import org.onlab.packet.MacAddress;
import org.onosproject.mastership.MastershipService;
import org.onosproject.net.device.DeviceEvent;
import org.onosproject.net.device.DeviceListener;
import org.onosproject.net.device.DeviceService;
import org.onosproject.net.flow.*;
import org.onosproject.net.packet.*;
import org.onosproject.p4tutorial.pipeconf.PipelineInterpreterImpl;
import org.osgi.service.component.annotations.Activate;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.Deactivate;
import org.osgi.service.component.annotations.Reference;
import org.osgi.service.component.annotations.ReferenceCardinality;
import org.onosproject.core.ApplicationId;
import org.onosproject.core.CoreService;
import org.onosproject.net.DeviceId;
import org.onosproject.net.Host;
import org.onosproject.net.PortNumber;
import org.onosproject.net.flow.criteria.PiCriterion;
import org.onosproject.net.host.HostEvent;
import org.onosproject.net.host.HostListener;
import org.onosproject.net.host.HostService;
import org.onosproject.net.pi.model.PiActionId;
import org.onosproject.net.pi.model.PiActionParamId;
import org.onosproject.net.pi.model.PiMatchFieldId;
import org.onosproject.net.pi.runtime.PiAction;
import org.onosproject.net.pi.runtime.PiActionParam;
import org.onosproject.net.topology.TopologyService;
import org.slf4j.Logger;

import java.nio.ByteBuffer;

import static org.slf4j.LoggerFactory.getLogger;

/**
 * L2 Switch Application
 * Flow Rule to build write request into the control engine
 * Packet-Out operation
 */
@Component(immediate = true)
public class L2SwitchApp {

    private static final String APP_NAME = "org.onosproject.p4tutorial.mytunnel";

    // Default priority used for flow rules installed by this app.
    private static final int FLOW_RULE_PRIORITY = 100;

    private final HostListener hostListener = new InternalHostListener();
    private ApplicationId appId;

    private static final Logger log = getLogger(L2SwitchApp.class);

    //--------------------------------------------------------------------------
    // ONOS core services needed by this application.
    //--------------------------------------------------------------------------

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    private FlowRuleService flowRuleService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    private CoreService coreService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    private TopologyService topologyService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    private HostService hostService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    protected PacketService packetService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    private MastershipService mastershipService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    private DeviceService deviceService;



    //--------------------------------------------------------------------------
    //--------------------------------------------------------------------------

    @Activate
    public void activate() {
        // Register app and event listeners.
        log.info("Starting...");
        appId = coreService.registerApplication(APP_NAME);
        hostService.addListener(hostListener);
        log.info("STARTED", appId.id());
        insertFlowRule(DeviceId.deviceId("device:bmv2:l2"));
        log.info("Added flowrule to switch: L2 Switch");
    }

    @Deactivate
    public void deactivate() {
        // Remove listeners and clean-up flow rules.
        log.info("Stopping...");
        hostService.removeListener(hostListener);
        flowRuleService.removeFlowRulesById(appId);
        log.info("STOPPED");
    }

    private void setUpDevice(DeviceId deviceId){
            }

    private void insertFlowRule(DeviceId deviceId){
        final int tableId = 0;
        final PiCriterion testMatch = PiCriterion.builder()
                .matchExact(PiMatchFieldId.of("hdr.ethernet.dst_addr"), MacAddress.valueOf("FF:FF:FF:FF:FF:FF").toBytes())
                .build();
        PortNumber portNumber = PortNumber.portNumber("1");
        final PiAction setAct = PiAction.builder()
                .withId(PiActionId.of("c_ingress.set_out_port"))
                .withParameter(new PiActionParam(PiActionParamId.of("port"), (short) portNumber.toLong()))
                .build();
        FlowRule rule = DefaultFlowRule.builder()
                .forDevice(deviceId)
                .forTable(tableId)
                .fromApp(appId)
                .withSelector(DefaultTrafficSelector.builder()
                        .matchPi(testMatch).build())
                .withTreatment(DefaultTrafficTreatment.builder()
                        .piTableAction(setAct).build())
                .makePermanent()
                .withPriority(FLOW_RULE_PRIORITY)
                .build();
        flowRuleService.applyFlowRules(rule);


	//Operation to build packet-out to send to the data plane
        TrafficTreatment treatment = DefaultTrafficTreatment.builder().setOutput(PortNumber.portNumber(255)).build();
        OutboundPacket outboundPacket;
        outboundPacket = new DefaultOutboundPacket(deviceId, treatment, ByteBuffer.wrap("\\377\\377\\377\\377\\377\\377\\000\\000\\000\\000\\000\\000\\220\\000\\000\\024\\0005\\000\\000\\000\\000\\000\\000\\000\\000P\\002 \\000\\000\\000\\000\\000E\\000\\000\\033\\000\\001\\000\\000@\\006|\\332\\177\\000\\000\\001\\177\\000\\000\\001Payload".getBytes()));
        packetService.emit(outboundPacket);

    }

    public class InternalDeviceListener implements DeviceListener {

        @Override
        public boolean isRelevant(DeviceEvent event) {
            switch (event.type()) {
                case DEVICE_ADDED:
                case DEVICE_AVAILABILITY_CHANGED:
                    break;
                default:
                    // Ignore other events.
                    return false;
            }
            // Process only if this controller instance is the master.
            final DeviceId deviceId = event.subject().id();
            return mastershipService.isLocalMaster(deviceId);
        }

        @Override
        public void event(DeviceEvent event) {
            final DeviceId deviceId = event.subject().id();
            if (deviceService.isAvailable(deviceId)) {
                // A P4Runtime device is considered available in ONOS when there
                // is a StreamChannel session open and the pipeline
                // configuration has been set.

                // Events are processed using a thread pool defined in the
                // MainComponent.
                setUpDevice(deviceId);
            }
        }
    }


    private static class InternalHostListener implements HostListener {

        @Override
        public void event(HostEvent event) {
            if (event.type() != HostEvent.Type.HOST_ADDED) {
                // Ignore other host events.
                return;
            }
            synchronized (this) {
                // Synchronizing here is an overkill, but safer for demo purposes.
                final Host host = event.subject();
                final DeviceId deviceId = host.location().deviceId();
                final PortNumber port = host.location().port();
            }
        }
    }


}
