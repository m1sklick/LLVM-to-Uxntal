//===-- UxnRegisterInfo.td - Uxn Register defs ---------*- tablegen -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//

//===----------------------------------------------------------------------===//
//  Declarations that describe the Uxn register file 
//===----------------------------------------------------------------------===//

class UxnReg<bits<16> Enc, string n> : Register<n> {
  let HWEncoding = Enc;
  let Namespace = "Uxn";
}

// CPU registers
def R0  : UxnReg< 0, "r0">;
def R1  : UxnReg< 1, "r1">;
def R2  : UxnReg< 2, "r2">;
def R3  : UxnReg< 3, "r3">;
def R4  : UxnReg< 4, "r4">;
def R5  : UxnReg< 5, "r5">;
def R6  : UxnReg< 6, "r6">;
def R7  : UxnReg< 7, "r7">;
def R8  : UxnReg< 8, "r8">;
def R9  : UxnReg< 9, "r9">;

def SP  : UxnReg<13, "sp">;
def LR  : UxnReg<14, "lr">;

def CPSR  : UxnReg<16, "cpsr">;

// Register classes.
//
def GRRegs : RegisterClass<"Uxn", [i32], 32,
  // Return values and arguments
  (add R0, R1, R2, R3,
       R4, R5, R6, R7, R8, R9, SP)>;
