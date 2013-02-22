/*
 * "THE WISKEY-WARE LICENSE":
 * <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
 * you can do whatever you want with this stuff. If we meet some day, and you
 * think this stuff is worth it, you can buy me a WISKEY us return.
 *
 */

var sigInst = null;

function init() {
    var sigRoot = document.getElementById('network');
    sigInst = sigma.init(sigRoot);
    addNode("puto", "puto", Math.random(), Math.random());
    sigInst.draw();
}

function addNode(id, label, x, y){
    sigInst.addNode(id, {label: label, x: x, y: y});
}

function addEdge(idf, idt, label){
    sigInst.addEdge(label, idf, idt);
}

if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", init, false);
} else {
    window.onload = init;
}
