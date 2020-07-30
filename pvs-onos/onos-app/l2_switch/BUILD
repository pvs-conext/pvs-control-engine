COMPILE_DEPS = CORE_DEPS + [
    "//apps/p4-tutorial/pipeconf:onos-apps-p4-tutorial-pipeconf",
    "@com_google_protobuf//:protobuf_java",
]

osgi_jar(
    deps = COMPILE_DEPS,
)

BUNDLES = [
    "//apps/p4-tutorial/l2_switch:onos-apps-p4-tutorial-l2_switch",
]

onos_app(
    app_name = "org.onosproject.p4tutorial.l2_switch",
    category = "Traffic Engineering",
    description = "Provides that installs l2 flow rules into the switch and does Packet I/O",
    included_bundles = BUNDLES,
    required_apps = [
        "org.onosproject.p4tutorial.pipeconf",
    ],
    title = "L2 Switch Demo App",
    url = "http://onosproject.org",
)
