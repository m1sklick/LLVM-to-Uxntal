//===-- UxnMachineFuctionInfo.h - Uxn machine function info -*- C++ -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//
//
// This file declares Uxn-specific per-machine-function information.
//
//===----------------------------------------------------------------------===//

#ifndef UxnMACHINEFUNCTIONINFO_H
#define UxnMACHINEFUNCTIONINFO_H

#include "llvm/CodeGen/MachineFrameInfo.h"
#include "llvm/CodeGen/MachineFunction.h"

namespace llvm {

// Forward declarations
class Function;

/// UxnFunctionInfo - This class is derived from MachineFunction private
/// Uxn target-specific information for each MachineFunction.
class UxnFunctionInfo : public MachineFunctionInfo {
public:
  UxnFunctionInfo() {}

  ~UxnFunctionInfo() {}
};
} // End llvm namespace

#endif // UxnMACHINEFUNCTIONINFO_H

