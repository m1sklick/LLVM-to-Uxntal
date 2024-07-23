//===-- UxnFixupKinds.h - Uxn-Specific Fixup Entries ------------*- C++ -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//

#ifndef LLVM_UxnFIXUPKINDS_H
#define LLVM_UxnFIXUPKINDS_H

#include "llvm/MC/MCFixup.h"

namespace llvm {
namespace Uxn {
enum Fixups {
  fixup_uxn_mov_hi16_pcrel = FirstTargetFixupKind,
  fixup_uxn_mov_lo16_pcrel,

  // Marker
  LastTargetFixupKind,
  NumTargetFixupKinds = LastTargetFixupKind - FirstTargetFixupKind
};
}
}

#endif

