/**
 * Created by tmackan on 16/5/10.
 */
var Fn = {

    hasVal: function (obj) {
        var val = $.trim($(obj).val());
        if (val.length > 0) {
            return true;
        } else {
            return false;
        }
    },

    hasPhone: function (obj) {
        var tel = $.trim($(obj).val());
        if (this.hasVal(obj)) {
            if ((/^13\d{9}$/g.test(tel)) || (/^15\d{9}$/g.test(tel))) {
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    },

    hasEmail: function (obj) {
        var ema = $.trim($(obj).val());
        var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
        if (this.hasVal(obj)) {
            if (reg.test(ema)) {
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    },

    isPhone: function (obj) {
        var tel = $.trim($(obj).val());
        if ((/^13\d{9}$/g.test(tel)) || (/^15\d{9}$/g.test(tel))) {
            return true;
        } else {
            return false;
        }
    },

     isEmail: function (obj) {
        var ema = $.trim($(obj).val());
        var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
        if (reg.test(ema)) {
            return true;
        } else {
            return false;
        }
    },

    isEqual: function (obj1, obj2) {
        var str1 = $.trim($(obj1).val());
        var str2 = $.trim($(obj2).val());
        if (str1 == str2) {
            return true;
        } else {
            return false;
        }
    },

    isNumber: function(obj) {
        var re = /^[0-9]+.?[0-9]*$/;

        if(!re.test($(obj).val())) {
            return false;
        } else {
            return true;
        }
    },

};