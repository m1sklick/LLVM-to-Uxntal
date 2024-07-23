//===-- UxnSelectionDAGInfo.h - Uxn SelectionDAG Info -------*- C++ -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//
//
// This file defines the Uxn subclass for TargetSelectionDAGInfo.
//
//===----------------------------------------------------------------------===//

#ifndef UxnSELECTIONDAGINFO_H
#define UxnSELECTIONDAGINFO_H

#include "llvm/Target/TargetSelectionDAGInfo.h"

namespace llvm {

class UxnSelectionDAGInfo : public TargetSelectionDAGInfo {
public:
  ~UxnSelectionDAGInfo();
};
}

#endif
