//===-- UxnTargetMachine.h - Define TargetMachine for Uxn ---*- C++ -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//
//
// This file declares the Uxn specific subclass of TargetMachine.
//
//===----------------------------------------------------------------------===//

#ifndef UxnTARGETMACHINE_H
#define UxnTARGETMACHINE_H

#include "Uxn.h"
#include "UxnFrameLowering.h"
#include "UxnISelLowering.h"
#include "UxnInstrInfo.h"
#include "UxnSelectionDAGInfo.h"
#include "UxnSubtarget.h"
#include "llvm/IR/DataLayout.h"
#include "llvm/Target/TargetMachine.h"

namespace llvm {

class UxnTargetMachine : public LLVMTargetMachine {
  UxnSubtarget Subtarget;
  std::unique_ptr<TargetLoweringObjectFile> TLOF;

public:
  UxnTargetMachine(const Target &T, const Triple &TT, StringRef CPU,
                   StringRef FS, const TargetOptions &Options, Reloc::Model RM,
                   CodeModel::Model CM, CodeGenOpt::Level OL);
  
  const UxnSubtarget * getSubtargetImpl() const {
    return &Subtarget;
  }
  
  virtual const TargetSubtargetInfo *
  getSubtargetImpl(const Function &) const override {
    return &Subtarget;
  }

  // Pass Pipeline Configuration
  virtual TargetPassConfig *createPassConfig(PassManagerBase &PM) override;
  
  TargetLoweringObjectFile *getObjFileLowering() const override {
    return TLOF.get();
  }
};

} // end namespace llvm

#endif
