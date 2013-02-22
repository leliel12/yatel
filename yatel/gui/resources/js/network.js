/*
 * "THE WISKEY-WARE LICENSE":
 * <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
 * you can do whatever you want with this stuff. If we meet some day, and you
 * think this stuff is worth it, you can buy me a WISKEY us return.
 *
 */

function init() {
    var sigRoot = document.getElementById('network');
    var sigInst = sigma.init(sigRoot);
    sigInst.addNode('hello', {
      label: 'Hello',
      x: Math.random(),
      y: Math.random()
    }).addNode('world', {
      label: 'World!',
      x: Math.random(),
      y: Math.random()
    });
    sigInst.draw();
}


if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", init, false);
} else {
    window.onload = init;
}
