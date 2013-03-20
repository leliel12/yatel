/*
 * "THE WISKEY-WARE LICENSE":
 * <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
 * you can do whatever you want with this stuff. If we meet some day, and you
 * think this stuff is worth it, you can buy me a WISKEY us return.
 *
 */


/*==============================================================================
 CONSTANTS
==============================================================================*/

var COLOR_FROM = {r: 32, g: 79, b: 25};
var COLOR_TO = {r: 180, g: 255, b: 158};


/*==============================================================================
 UTILS
==============================================================================*/

/* var python <<< this is changed from python with only one method emit */

var utils = {
    choice: function(arr){
        var rand = Math.random();
        rand *= arr.length;
        rand = Math.floor(rand);
        return arr[rand];
    },
    getRandomColor: function(){
        var a = COLOR_FROM;
        var b = COLOR_TO;
        var r = Math.random();
            return 'rgb('+
            ((a.r+(b.r-a.r)*r)|0).toString() + ','+
            ((a.g+(b.g-a.g)*r)|0).toString() + ','+
            ((a.b+(b.b-a.b)*r)|0).toString() + ')';
    }
}


/*==============================================================================
 MAIN  CLASS
==============================================================================*/




/*==============================================================================
 INITS
==============================================================================*/

function init(rootid){
    ;
    //network.addNode('hap0', 'hap0', 0, 20);
}
