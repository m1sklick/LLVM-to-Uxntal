//===-- UxnMCTargetDesc.cpp - Uxn Target Descriptions -----------------===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//
//
// This file provides Uxn specific target descriptions.
//
//===----------------------------------------------------------------------===//

#include "UxnMCTargetDesc.h"
#include "InstPrinter/UxnInstPrinter.h"
#include "UxnMCAsmInfo.h"
#include "llvm/MC/MCCodeGenInfo.h"
#include "llvm/MC/MCInstrInfo.h"
#include "llvm/MC/MCRegisterInfo.h"
#include "llvm/MC/MCSubtargetInfo.h"
#include "llvm/MC/MCStreamer.h"
#include "llvm/Support/ErrorHandling.h"
#include "llvm/Support/FormattedStream.h"
#include "llvm/Support/TargetRegistry.h"

#define GET_INSTRINFO_MC_DESC
#include "UxnGenInstrInfo.inc"

#define GET_SUBTARGETINFO_MC_DESC
#include "UxnGenSubtargetInfo.inc"

#define GET_REGINFO_MC_DESC
#include "UxnGenRegisterInfo.inc"

using namespace llvm;

static MCInstrInfo *createUxnMCInstrInfo() {
  MCInstrInfo *X = new MCInstrInfo();
  InitUxnMCInstrInfo(X);
  return X;
}

static MCRegisterInfo *createUxnMCRegisterInfo(const Triple &TT) {
  MCRegisterInfo *X = new MCRegisterInfo();
  InitUxnMCRegisterInfo(X, Uxn::LR);
  return X;
}

static MCSubtargetInfo *createUxnMCSubtargetInfo(const Triple &TT,
                                                 StringRef CPU,
                                                 StringRef FS) {
  return createUxnMCSubtargetInfoImpl(TT, CPU, FS);
}

static MCAsmInfo *createUxnMCAsmInfo(const MCRegisterInfo &MRI,
                                     const Triple &TT) {
  return new UxnMCAsmInfo(TT);
}

static MCCodeGenInfo *createUxnMCCodeGenInfo(const Triple &TT, Reloc::Model RM,
                                             CodeModel::Model CM,
                                             CodeGenOpt::Level OL) {
  MCCodeGenInfo *X = new MCCodeGenInfo();
  if (RM == Reloc::Default) {
    RM = Reloc::Static;
  }
  if (CM == CodeModel::Default) {
    CM = CodeModel::Small;
  }
  if (CM != CodeModel::Small && CM != CodeModel::Large) {
    report_fatal_error("Target only supports CodeModel Small or Large");
  }

  X->initMCCodeGenInfo(RM, CM, OL);
  return X;
}

static MCInstPrinter *
createUxnMCInstPrinter(const Triple &TT, unsigned SyntaxVariant,
                       const MCAsmInfo &MAI, const MCInstrInfo &MII,
                       const MCRegisterInfo &MRI) {
  return new UxnInstPrinter(MAI, MII, MRI);
}

// Force static initialization.
extern "C" void LLVMInitializeUxnTargetMC() {
  // Register the MC asm info.
  RegisterMCAsmInfoFn X(TheUxnTarget, createUxnMCAsmInfo);

  // Register the MC codegen info.
  TargetRegistry::RegisterMCCodeGenInfo(TheUxnTarget, createUxnMCCodeGenInfo);

  // Register the MC instruction info.
  TargetRegistry::RegisterMCInstrInfo(TheUxnTarget, createUxnMCInstrInfo);

  // Register the MC register info.
  TargetRegistry::RegisterMCRegInfo(TheUxnTarget, createUxnMCRegisterInfo);

  // Register the MC subtarget info.
  TargetRegistry::RegisterMCSubtargetInfo(TheUxnTarget,
                                          createUxnMCSubtargetInfo);

  // Register the MCInstPrinter
  TargetRegistry::RegisterMCInstPrinter(TheUxnTarget, createUxnMCInstPrinter);

  // Register the ASM Backend.
  TargetRegistry::RegisterMCAsmBackend(TheUxnTarget, createUxnAsmBackend);

  // Register the MCCodeEmitter
  TargetRegistry::RegisterMCCodeEmitter(TheUxnTarget, createUxnMCCodeEmitter);
}
