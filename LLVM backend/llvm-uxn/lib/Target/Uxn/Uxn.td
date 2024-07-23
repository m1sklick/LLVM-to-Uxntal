//===-- Uxn.td - Describe the Uxn Target Machine -------*- tablegen -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//
//
// This is the top level entry point for the Uxn target.
//
//===----------------------------------------------------------------------===//

//===----------------------------------------------------------------------===//
// Target-independent interfaces which we are implementing
//===----------------------------------------------------------------------===//

include "llvm/Target/Target.td"

//===----------------------------------------------------------------------===//
// Descriptions
//===----------------------------------------------------------------------===//

include "UxnRegisterInfo.td"
include "UxnInstrInfo.td"
include "UxnCallingConv.td"

def UxnInstrInfo : InstrInfo;

//===----------------------------------------------------------------------===//
// Uxn processors supported.
//===----------------------------------------------------------------------===//

class Proc<string Name, list<SubtargetFeature> Features>
    : Processor<Name, NoItineraries, Features>;

def : Proc<"generic", []>;

//===----------------------------------------------------------------------===//
// Declare the target which we are implementing
//===----------------------------------------------------------------------===//

def Uxn : Target {
  let InstructionSet = UxnInstrInfo;
}
