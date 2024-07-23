//===-- UxnELFObjectWriter.cpp - Uxn ELF Writer ---------------------------===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//

#include "MCTargetDesc/UxnMCTargetDesc.h"
#include "MCTargetDesc/UxnFixupKinds.h"
#include "llvm/ADT/Statistic.h"
#include "llvm/ADT/StringSwitch.h"
#include "llvm/MC/MCELFObjectWriter.h"
#include "llvm/MC/MCExpr.h"
#include "llvm/MC/MCSectionELF.h"
#include "llvm/MC/MCValue.h"
#include "llvm/Support/Debug.h"
#include "llvm/Support/ErrorHandling.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

namespace {
  class UxnELFObjectWriter : public MCELFObjectTargetWriter {
  public:
    UxnELFObjectWriter(uint8_t OSABI);

    virtual ~UxnELFObjectWriter();

    unsigned GetRelocType(const MCValue &Target, const MCFixup &Fixup,
                          bool IsPCRel) const override;
  };
}

unsigned UxnELFObjectWriter::GetRelocType(const MCValue &Target,
                                          const MCFixup &Fixup,
                                          bool IsPCRel) const {
  if (!IsPCRel) {
    llvm_unreachable("Only dealying with PC-relative fixups for now");
  }

  unsigned Type = 0;
  switch ((unsigned)Fixup.getKind()) {
  default:
    llvm_unreachable("Unimplemented");
  case Uxn::fixup_uxn_mov_hi16_pcrel:
    Type = ELF::R_ARM_MOVT_PREL;
    break;
  case Uxn::fixup_uxn_mov_lo16_pcrel:
    Type = ELF::R_ARM_MOVW_PREL_NC;
    break;
  }
  return Type;
}

UxnELFObjectWriter::UxnELFObjectWriter(uint8_t OSABI)
    : MCELFObjectTargetWriter(/*Is64Bit*/ false, OSABI, /*ELF::EM_Uxn*/ ELF::EM_ARM,
                              /*HasRelocationAddend*/ false) {}

UxnELFObjectWriter::~UxnELFObjectWriter() {}

MCObjectWriter *llvm::createUxnELFObjectWriter(raw_pwrite_stream &OS, uint8_t OSABI) {
  MCELFObjectTargetWriter *MOTW = new UxnELFObjectWriter(OSABI);
  return createELFObjectWriter(MOTW, OS, /*IsLittleEndian=*/true);
}
