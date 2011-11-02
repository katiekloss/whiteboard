jQuery.fn.form2json = function() {
    var $formNames = $(this[0]).serializeArray();
    var $formAssoc = {};
    $formNames.map(function(input) {
        if(!(input.name in $formAssoc)) {
            $formAssoc[input.name] = input.value;
        } else {
            if($formAssoc[input.name] instanceof Array) {
                $formAssoc[input.name].push(input.value);
            } else {
                $formAssoc[input.name] = new Array($formAssoc[input.name], input.value);
            }
        }
    });
    return JSON.stringify($formAssoc);
}
