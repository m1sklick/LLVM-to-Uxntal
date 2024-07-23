set(LLVM_TARGET_DEFINITIONS Uxn.td)

tablegen(LLVM UxnGenRegisterInfo.inc -gen-register-info)
tablegen(LLVM UxnGenInstrInfo.inc -gen-instr-info)
tablegen(LLVM UxnGenAsmWriter.inc -gen-asm-writer)
tablegen(LLVM UxnGenDAGISel.inc -gen-dag-isel)
tablegen(LLVM UxnGenCallingConv.inc -gen-callingconv)
tablegen(LLVM UxnGenSubtargetInfo.inc -gen-subtarget)
tablegen(LLVM UxnGenMCCodeEmitter.inc -gen-emitter)
add_public_tablegen_target(UxnCommonTableGen)

add_llvm_target(UxnCodeGen
  UxnSubtarget.cpp
  UxnTargetMachine.cpp
  UxnRegisterInfo.cpp
  UxnInstrInfo.cpp
  UxnFrameLowering.cpp
  UxnISelLowering.cpp
  UxnSelectionDAGInfo.cpp
  UxnISelDAGToDAG.cpp
  UxnAsmPrinter.cpp
  UxnMCInstLower.cpp
  )

add_subdirectory(InstPrinter)
add_subdirectory(TargetInfo)
add_subdirectory(MCTargetDesc)
