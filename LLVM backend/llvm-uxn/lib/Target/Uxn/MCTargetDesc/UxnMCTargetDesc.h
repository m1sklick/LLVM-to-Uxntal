//===-- UxnMCTargetDesc.h - Uxn Target Descriptions ---------*- C++ -*-===//
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

#ifndef UxnMCTARGETDESC_H
#define UxnMCTARGETDESC_H

#include "llvm/Support/DataTypes.h"

namespace llvm {
class Target;
class MCInstrInfo;
class MCRegisterInfo;
class MCSubtargetInfo;
class MCContext;
class MCCodeEmitter;
class MCAsmInfo;
class MCCodeGenInfo;
class MCInstPrinter;
class MCObjectWriter;
class MCAsmBackend;

class StringRef;
class raw_ostream;
class raw_pwrite_stream;
class Triple;

extern Target TheUxnTarget;

MCCodeEmitter *createUxnMCCodeEmitter(const MCInstrInfo &MCII,
                                      const MCRegisterInfo &MRI,
                                      MCContext &Ctx);

MCAsmBackend *createUxnAsmBackend(const Target &T, const MCRegisterInfo &MRI,
                                  const Triple &TT, StringRef CPU);

MCObjectWriter *createUxnELFObjectWriter(raw_pwrite_stream &OS, uint8_t OSABI);

} // End llvm namespace

// Defines symbolic names for Uxn registers.  This defines a mapping from
// register name to register number.
//
#define GET_REGINFO_ENUM
#include "UxnGenRegisterInfo.inc"

// Defines symbolic names for the Uxn instructions.
//
#define GET_INSTRINFO_ENUM
#include "UxnGenInstrInfo.inc"

#define GET_SUBTARGETINFO_ENUM
#include "UxnGenSubtargetInfo.inc"

#endif
