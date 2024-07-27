//===-- UxnRegisterInfo.cpp - Uxn Register Information ----------------===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//
//
// This file contains the Uxn implementation of the MRegisterInfo class.
//
//===----------------------------------------------------------------------===//

#include "UxnRegisterInfo.h"
#include "Uxn.h"
#include "UxnFrameLowering.h"
#include "UxnInstrInfo.h"
#include "UxnMachineFunctionInfo.h"
#include "llvm/ADT/BitVector.h"
#include "llvm/ADT/STLExtras.h"
#include "llvm/CodeGen/MachineFrameInfo.h"
#include "llvm/CodeGen/MachineFunction.h"
#include "llvm/CodeGen/MachineInstrBuilder.h"
#include "llvm/CodeGen/MachineModuleInfo.h"
#include "llvm/CodeGen/MachineRegisterInfo.h"
#include "llvm/CodeGen/RegisterScavenging.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/Type.h"
#include "llvm/Support/Debug.h"
#include "llvm/Support/ErrorHandling.h"
#include "llvm/Support/MathExtras.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Target/TargetFrameLowering.h"
#include "llvm/Target/TargetMachine.h"
#include "llvm/Target/TargetOptions.h"

#define GET_REGINFO_TARGET_DESC
#include "UxnGenRegisterInfo.inc"

using namespace llvm;

UxnRegisterInfo::UxnRegisterInfo() : UxnGenRegisterInfo(Uxn::LR) {}

const uint16_t *
UxnRegisterInfo::getCalleeSavedRegs(const MachineFunction *MF) const {
  static const uint16_t CalleeSavedRegs[] = { Uxn::R4, Uxn::R5, Uxn::R6,
                                              Uxn::R7, Uxn::R8, Uxn::R9,
                                              0 };
  return CalleeSavedRegs;
}

BitVector UxnRegisterInfo::getReservedRegs(const MachineFunction &MF) const {
  BitVector Reserved(getNumRegs());

  Reserved.set(Uxn::SP);
  Reserved.set(Uxn::LR);
  return Reserved;
}

const uint32_t *UxnRegisterInfo::getCallPreservedMask(const MachineFunction &MF,
                                                      CallingConv::ID) const {
  return CC_Save_RegMask;
}

bool
UxnRegisterInfo::requiresRegisterScavenging(const MachineFunction &MF) const {
  return true;
}

bool
UxnRegisterInfo::trackLivenessAfterRegAlloc(const MachineFunction &MF) const {
  return true;
}

bool UxnRegisterInfo::useFPForScavengingIndex(const MachineFunction &MF) const {
  return false;
}

void UxnRegisterInfo::eliminateFrameIndex(MachineBasicBlock::iterator II,
                                          int SPAdj, unsigned FIOperandNum,
                                          RegScavenger *RS) const {
  MachineInstr &MI = *II;
  const MachineFunction &MF = *MI.getParent()->getParent();
  const MachineFrameInfo *MFI = MF.getFrameInfo();
  MachineOperand &FIOp = MI.getOperand(FIOperandNum);
  unsigned FI = FIOp.getIndex();

  // Determine if we can eliminate the index from this kind of instruction.
  unsigned ImmOpIdx = 0;
  switch (MI.getOpcode()) {
  default:
    // Not supported yet.
    return;
  case Uxn::LDR:
  case Uxn::STR:
    ImmOpIdx = FIOperandNum + 1;
    break;
  }

  // FIXME: check the size of offset.
  MachineOperand &ImmOp = MI.getOperand(ImmOpIdx);
  int Offset = MFI->getObjectOffset(FI) + MFI->getStackSize() + ImmOp.getImm();
  FIOp.ChangeToRegister(Uxn::SP, false);
  ImmOp.setImm(Offset);
}

unsigned UxnRegisterInfo::getFrameRegister(const MachineFunction &MF) const {
  return Uxn::SP;
}
