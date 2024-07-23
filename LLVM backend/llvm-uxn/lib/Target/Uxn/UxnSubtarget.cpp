//===-- UxnSubtarget.cpp - Uxn Subtarget Information ------------------===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//
//
// This file implements the Uxn specific subclass of TargetSubtargetInfo.
//
//===----------------------------------------------------------------------===//

#include "UxnSubtarget.h"
#include "Uxn.h"
#include "llvm/Support/TargetRegistry.h"

#define DEBUG_TYPE "uxn-subtarget"

#define GET_SUBTARGETINFO_TARGET_DESC
#define GET_SUBTARGETINFO_CTOR
#include "UxnGenSubtargetInfo.inc"

using namespace llvm;

void UxnSubtarget::anchor() {}

UxnSubtarget::UxnSubtarget(const Triple &TT, StringRef CPU, StringRef FS,
                           UxnTargetMachine &TM)
    : UxnGenSubtargetInfo(TT, CPU, FS),
      DL("e-m:e-p:32:32-i1:8:32-i8:8:32-i16:16:32-i64:32-f64:32-a:0:32-n32"),
      InstrInfo(), TLInfo(TM), TSInfo(), FrameLowering() {}
