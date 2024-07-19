#ifndef EvaLLVM_h
#define EvaLLVM_h

#include <string>

#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Module.h"

class EvaLLVM {
    public:
        EvaLLVM() { moduleInit(); }

        void exec(const std::string& program){
            // 1. Prase the program
            // auto ast = parser->parser(program;
            
            // 2. Compile ot LLVM IR
            // compile(ast);

            // 3. Save module IR to file
            saveModuleToFile("./out.ll");
        }

    private:

    void saveModuleToFile(const std::string& fileName) {
        std::error_code errorCode;
        llvm::raw_fd_ostream outLL(fileName, errorCode);
        module->print(outLL, nullptr);
    }

    void moduleInit() {

        ctx = std::make_unique<llvm::LLVMContext>();
        module = std::make_unique<llvm::Module>("EvaLLVM", *ctx);

        builder = std::make_unique<llvm::IRBuilder<>>(*ctx);

    }

    std::unique_ptr<llvm::LLVMContext> ctx;

    std::unique_ptr<llvm::Module> module;

    std::unique_ptr<llvm::IRBuilder<>> builder;

};

#endif