# unikernel {#unikernel}

* https://en.wikipedia.org/wiki/Unikernel
  * http://rumpkernel.org/
    * https://en.wikipedia.org/wiki/Rump_kernel
* https://github.com/dom96/nimkernel

***

* runs under virtualization hypervisor
  * minimal code, single address space
* combined from a set of libraries, LTO linker removes all unused code
* uses @ref tcc for i386/x32 target (compact code)
  * multiple distributed nodes with not more than 1..2G RAM are preferred
