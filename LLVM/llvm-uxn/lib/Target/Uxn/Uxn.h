//===-- Uxn.h - Top-level interface for Uxn representation --*- C++ -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//
//
// This file contains the entry points for global functions defined in the LLVM
// Uxn back-end.
//
//===----------------------------------------------------------------------===//

#ifndef TARGET_Uxn_H
#define TARGET_Uxn_H

#include "MCTargetDesc/UxnMCTargetDesc.h"
#include "llvm/Target/TargetMachine.h"

namespace llvm {
class TargetMachine;
class UxnTargetMachine;

FunctionPass *createUxnISelDag(UxnTargetMachine &TM,
                               CodeGenOpt::Level OptLevel);
} // end namespace llvm;

#endif
