//
// Copyright (c) 2017 Stephen Ibanez
// All rights reserved.
//
// This software was developed by Stanford University and the University of Cambridge Computer Laboratory 
// under National Science Foundation under Grant No. CNS-0855268,
// the University of Cambridge Computer Laboratory under EPSRC INTERNET Project EP/H040536/1 and
// by the University of Cambridge Computer Laboratory under DARPA/AFRL contract FA8750-11-C-0249 ("MRC2"), 
// as part of the DARPA MRC research programme.
//
// @NETFPGA_LICENSE_HEADER_START@
//
// Licensed to NetFPGA C.I.C. (NetFPGA) under one or more contributor
// license agreements.  See the NOTICE file distributed with this work for
// additional information regarding copyright ownership.  NetFPGA licenses this
// file to you under the NetFPGA Hardware-Software License, Version 1.0 (the
// "License"); you may not use this file except in compliance with the
// License.  You may obtain a copy of the License at:
//
//   http://www.netfpga-cic.org
//
// Unless required by applicable law or agreed to in writing, Work distributed
// under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
// CONDITIONS OF ANY KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations under the License.
//
// @NETFPGA_LICENSE_HEADER_END@
//


/*
 * File: 
 * Author: Stephen Ibanez
 *
 * This file provides the declarations for some convenience functions that
 * that can be used when working with SDNet generated TCAM tables.
 */

#ifndef LIBTCAM_H
#define LIBTCAM_H

int tcam_clean(uint32_t tableID);

uint32_t tcam_get_addr_size();

int tcam_set_log_level(uint32_t tableID, unit32_t msg_level);

int tcam_write_entry(uint32_t tableID, uint32_t addr, const char* data, const char* mask, const char* value);

int tcam_erase_entry(uint32_t tableID, uint32_t addr);

uint32_t tcam_verify_entry(uint32_t tableID, uint32_t addr, const char* data, const char* mask, const char* value);

const char* tcam_error_decode(int error);

#endif // LIBTCAM_H 

