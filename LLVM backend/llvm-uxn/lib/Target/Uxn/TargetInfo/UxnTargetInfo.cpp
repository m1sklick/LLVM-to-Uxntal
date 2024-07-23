//===-- UxnTargetInfo.cpp - Uxn Target Implementation -----------------===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//

#include "Uxn.h"
#include "llvm/IR/Module.h"
#include "llvm/Support/TargetRegistry.h"
using namespace llvm;

Target llvm::TheUxnTarget;

extern "C" void LLVMInitializeUxnTargetInfo() {
  RegisterTarget<Triple::uxn> X(TheUxnTarget, "uxn", "Uxn");
}
