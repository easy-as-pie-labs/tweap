/**
 * shorthand logging function
 * also adds compatiblity to super old opera ;)
 */
function log() {
    // tries usual logging
    try {
        console.log.apply(console, arguments);
    }
    catch(e) {
        // tries logging the opera way
        try {
            opera.postError.apply(opera, arguments);
        }
        catch(e) {
            // if all hell breaks loose, alerts!!

            // let's disable this in case someone forgets to take out logs
            //alert(Array.prototype.join.call(arguments, " "));
        }
    }
}