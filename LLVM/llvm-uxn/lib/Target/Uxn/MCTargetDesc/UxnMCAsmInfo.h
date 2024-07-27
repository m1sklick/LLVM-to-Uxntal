//===-- UxnMCAsmInfo.h - Uxn asm properties --------------------*- C++ -*--===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//
//
// This file contains the declaration of the UxnMCAsmInfo class.
//
//===----------------------------------------------------------------------===//

#ifndef UxnTARGETASMINFO_H
#define UxnTARGETASMINFO_H

#include "llvm/MC/MCAsmInfoELF.h"

namespace llvm {
class StringRef;
class Target;
class Triple;

class UxnMCAsmInfo : public MCAsmInfoELF {
  virtual void anchor();

public:
  explicit UxnMCAsmInfo(const Triple &TT);
};

} // namespace llvm

#endif
