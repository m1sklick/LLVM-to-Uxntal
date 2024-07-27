//===-- UxnTargetMachine.cpp - Define TargetMachine for Uxn -----------===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//
//
//
//===----------------------------------------------------------------------===//

#include "UxnTargetMachine.h"
#include "Uxn.h"
#include "UxnFrameLowering.h"
#include "UxnInstrInfo.h"
#include "UxnISelLowering.h"
#include "UxnSelectionDAGInfo.h"
#include "llvm/CodeGen/Passes.h"
#include "llvm/CodeGen/TargetLoweringObjectFileImpl.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/PassManager.h"
#include "llvm/Support/TargetRegistry.h"

using namespace llvm;

static std::string computeDataLayout(const Triple &TT, StringRef CPU,
                                     const TargetOptions &Options) {
  // XXX Build the triple from the arguments.
  // This is hard-coded for now for this example target.
  return "e-m:e-p:32:32-i1:8:32-i8:8:32-i16:16:32-i64:32-f64:32-a:0:32-n32";
}

UxnTargetMachine::UxnTargetMachine(const Target &T, const Triple &TT,
                                   StringRef CPU, StringRef FS,
                                   const TargetOptions &Options,
                                   Reloc::Model RM, CodeModel::Model CM,
                                   CodeGenOpt::Level OL)
    : LLVMTargetMachine(T, computeDataLayout(TT, CPU, Options), TT, CPU, FS,
                        Options, RM, CM, OL),
      Subtarget(TT, CPU, FS, *this),
      TLOF(make_unique<TargetLoweringObjectFileELF>()) {
  initAsmInfo();
}

namespace {
/// Uxn Code Generator Pass Configuration Options.
class UxnPassConfig : public TargetPassConfig {
public:
  UxnPassConfig(UxnTargetMachine *TM, PassManagerBase &PM)
      : TargetPassConfig(TM, PM) {}

  UxnTargetMachine &getUxnTargetMachine() const {
    return getTM<UxnTargetMachine>();
  }

  virtual bool addPreISel() override;
  virtual bool addInstSelector() override;
  virtual void addPreEmitPass() override;
};
} // namespace

TargetPassConfig *UxnTargetMachine::createPassConfig(PassManagerBase &PM) {
  return new UxnPassConfig(this, PM);
}

bool UxnPassConfig::addPreISel() { return false; }

bool UxnPassConfig::addInstSelector() {
  addPass(createUxnISelDag(getUxnTargetMachine(), getOptLevel()));
  return false;
}

void UxnPassConfig::addPreEmitPass() {}

// Force static initialization.
extern "C" void LLVMInitializeUxnTarget() {
  RegisterTargetMachine<UxnTargetMachine> X(TheUxnTarget);
}
