var killErrors = function (value) {
    return true
};
window.onerror = null;
window.onerror = killErrors;
var base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
var base64DecodeChars = new Array(-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1);

function base64encode(str) {
    var out, i, len;
    var c1, c2, c3;
    len = str.length;
    i = 0;
    out = "";
    while (i < len) {
        c1 = str.charCodeAt(i++) & 0xff;
        if (i == len) {
            out += base64EncodeChars.charAt(c1 >> 2);
            out += base64EncodeChars.charAt((c1 & 0x3) << 4);
            out += "==";
            break
        }
        c2 = str.charCodeAt(i++);
        if (i == len) {
            out += base64EncodeChars.charAt(c1 >> 2);
            out += base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
            out += base64EncodeChars.charAt((c2 & 0xF) << 2);
            out += "=";
            break
        }
        c3 = str.charCodeAt(i++);
        out += base64EncodeChars.charAt(c1 >> 2);
        out += base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
        out += base64EncodeChars.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6));
        out += base64EncodeChars.charAt(c3 & 0x3F)
    }
    return out
}

function base64decode(str) {
    var c1, c2, c3, c4;
    var i, len, out;
    len = str.length;
    i = 0;
    out = "";
    while (i < len) {
        do {
            c1 = base64DecodeChars[str.charCodeAt(i++) & 0xff]
        } while (i < len && c1 == -1);
        if (c1 == -1) break;
        do {
            c2 = base64DecodeChars[str.charCodeAt(i++) & 0xff]
        } while (i < len && c2 == -1);
        if (c2 == -1) break;
        out += String.fromCharCode((c1 << 2) | ((c2 & 0x30) >> 4));
        do {
            c3 = str.charCodeAt(i++) & 0xff;
            if (c3 == 61) return out;
            c3 = base64DecodeChars[c3]
        } while (i < len && c3 == -1);
        if (c3 == -1) break;
        out += String.fromCharCode(((c2 & 0XF) << 4) | ((c3 & 0x3C) >> 2));
        do {
            c4 = str.charCodeAt(i++) & 0xff;
            if (c4 == 61) return out;
            c4 = base64DecodeChars[c4]
        } while (i < len && c4 == -1);
        if (c4 == -1) break;
        out += String.fromCharCode(((c3 & 0x03) << 6) | c4)
    }
    return out
}

function utf16to8(str) {
    var out, i, len, c;
    out = "";
    len = str.length;
    for (i = 0; i < len; i++) {
        c = str.charCodeAt(i);
        if ((c >= 0x0001) && (c <= 0x007F)) {
            out += str.charAt(i)
        } else if (c > 0x07FF) {
            out += String.fromCharCode(0xE0 | ((c >> 12) & 0x0F));
            out += String.fromCharCode(0x80 | ((c >> 6) & 0x3F));
            out += String.fromCharCode(0x80 | ((c >> 0) & 0x3F))
        } else {
            out += String.fromCharCode(0xC0 | ((c >> 6) & 0x1F));
            out += String.fromCharCode(0x80 | ((c >> 0) & 0x3F))
        }
    }
    return out
}

function utf8to16(str) {
    var out, i, len, c;
    var char2, char3;
    out = "";
    len = str.length;
    i = 0;
    while (i < len) {
        c = str.charCodeAt(i++);
        switch (c >> 4) {
            case 0:
            case 1:
            case 2:
            case 3:
            case 4:
            case 5:
            case 6:
            case 7:
                out += str.charAt(i - 1);
                break;
            case 12:
            case 13:
                char2 = str.charCodeAt(i++);
                out += String.fromCharCode(((c & 0x1F) << 6) | (char2 & 0x3F));
                break;
            case 14:
                char2 = str.charCodeAt(i++);
                char3 = str.charCodeAt(i++);
                out += String.fromCharCode(((c & 0x0F) << 12) | ((char2 & 0x3F) << 6) | ((char3 & 0x3F) << 0));
                break
        }
    }
    return out
}
eval(function (p, a, c, k, e, r) {
    e = function (c) {
        return (c < a ? '' : e(parseInt(c / a))) + ((c = c % a) > 35 ? String.fromCharCode(c + 29) : c.toString(36))
    };
    if (!''.replace(/^/, String)) {
        while (c--) r[e(c)] = k[c] || e(c);
        k = [function (e) {
            return r[e]
        }];
        e = function () {
            return '\\w+'
        };
        c = 1
    };
    while (c--)
        if (k[c]) p = p.replace(new RegExp('\\b' + e(c) + '\\b', 'g'), k[c]);
    return p
}('C c={\'1i\':7(s,n){2A 3.1e.w(\'{1b}\',s).w(\'{1b}\',s).w(\'{1a}\',n).w(\'{1a}\',n)},\'1X\':7(s,n){1U.1T=3.1i(s,n)},\'1S\':7(){$(\'#i\').H(\'e\',3.17);1P(7(){c.13()},3.U*1o);$("#D").E(0).1n=3.2C+\'\';C a=r.2y(\'Q\');a.2e=\'2b/22\';a.1R=O;a.1u=\'1t-8\';a.e=\'\';C b=r.1I(\'Q\')[0];b.1p.1r(a,b)},\'1s\':7(){6($("#i").H(\'e\')!=3.G){$("#i").H(\'e\',3.G)}$("#i").10()},\'13\':7(){$(\'#i\').2p()},\'1l\':7(){3.K=1q;$(\'#L\').10()},\'M\':7(){r.N(\'<p>.c{1v: #1C;1G-1H:1J;1K:#1L;1N:P;1Q:P;x:1V;1W:21;j:\'+3.k+\';f:\'+3.l+\';2q-f:2x;}.c F{j:9%;f:9%;}.c #D{x:1j;!1k;j:9%;f:9%;}</p><R 1m="c">\'+\'<t A="i" e="" S="0" T="B" j="9%" f="9%" p="x:V;z-W:X;"></t><t A="L" e="" S="0" T="B" j="9%" f="9%" p="x:V;z-W:X;1w:1x;"></t>\'+\'<F 1y="0" 1z="0" 1A="0"><1B><Y A="D" 1D="1E" p="">&1F;</Y></F></R>\');3.Z=$(\'.c\').E(0).Z;3.I=$(\'.c\').E(0).I;r.N(\'<J\'+\'11 e="\'+3.12+3.h+\'.1M"></J\'+\'11>\')},\'14\':7(){},\'1O\':7(){3.K=O;3.15=\'\';6(4.16==\'1\'){4.m=q(4.m);4.o=q(4.o)}18 6(4.16==\'2\'){4.m=q(19(4.m));4.o=q(19(4.o))}3.g=1Y.1Z.20();3.k=5.j;3.l=5.f;6(3.g.d("23")>0||3.g.d("24")>0||3.g.d("25")>0||3.g.d("26")>0||3.g.d("27")>0||3.g.d("28")>0){3.k=5.29;3.l=5.2a}6(3.k.d("1c")==-1&&3.k.d("%")==-1){3.k=\'9%\'}6(3.l.d("1c")==-1&&3.l.d("%")==-1){3.l=\'9%\'}3.17=5.2c;3.G=5.i;3.U=5.2d;3.1d=4.2f;3.2g=4.2h;3.2i=4.2j;3.1e=2k(4.2l);3.h=4.2m;3.2n=4.2o;3.v=4.1f==\'B\'?\'\':4.1f;3.2r=4.m;3.2s=4.o;3.2t=4.2u;3.2v=4.2w;6(5.1g[3.v]!=1h){3.v=5.1g[3.v].2z}6(5.u[3.h]!=1h){6(5.u[3.h].2B=="1"){3.15=5.u[3.h].y==\'\'?5.y:5.u[3.h].y;3.h=\'y\'}}3.12=2D.2E+\'/2F/2G/\';6(3.1d=="2H"){c.14()}18{c.M()}}};', 62, 168, '|||this|player_data|MacPlayerConfig|if|function||100|||MacPlayer|indexOf|src|height|Agent|PlayFrom|buffer|width|Width|Height|url||url_next|style|unescape|document||iframe|player_list|PlayServer|replace|position|parse||id|no|var|playleft|get|table|Buffer|attr|offsetWidth|scr|Status|install|Play|write|true|0px|script|div|frameBorder|scrolling|Second|absolute|index|99998|td|offsetHeight|show|ipt|Path|AdsEnd|Down|Parse|encrypt|Prestrain|else|base64decode|nid|sid|px|Flag|Link|server|server_list|undefined|GetUrl|inherit|important|Install|class|innerHTML|1000|parentNode|false|insertBefore|AdsStart|utf|charset|background|display|none|border|cellpadding|cellspacing|tr|000000|valign|top|nbsp|font|size|getElementsByTagName|14px|color|F6F6F6|js|margin|Init|setTimeout|padding|async|Show|href|location|relative|overflow|Go|navigator|userAgent|toLowerCase|hidden|javascript|android|mobile|ipod|ios|iphone|ipad|widthmob|heightmob|text|prestrain|second|type|flag|Trysee|trysee|Points|points|decodeURIComponent|link|from|PlayNote|note|hide|min|PlayUrl|PlayUrlNext|PlayLinkNext|link_next|PlayLinkPre|link_pre|100px|createElement|des|return|ps|Html|maccms|path|static|player|down'.split('|'), 0, {}))
MacPlayer.Init();