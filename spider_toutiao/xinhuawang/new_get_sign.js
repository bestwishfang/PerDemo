function get_signature(behot) {
  function e(e, a, r) {
      return (b[e] || (b[e] = t("x,y", "return x " + e + " y")))(r, a)
  }
  function a(e, a, r) {
      return (k[r] || (k[r] = t("x,y", "return new x[y](" + Array(r + 1).join(",x[++y]").substr(1) + ")")))(e, a)
  }
  function r(e, a, r) {
      var n, t, s = {},
      b = s.d = r ? r.d + 1 : 0;
      for (s["$" + b] = s, t = 0; t < b; t++) s[n = "$" + t] = r[n];
      for (t = 0, b = s.length = a.length; t < b; t++) s[t] = a[t];
      return c(e, 0, s)
  }
  function c(t, b, k) {
      function u(e) {
          v[x++] = e
      }
      function f() {
          return g = t.charCodeAt(b++) - 32,
          t.substring(b, b += g)
      }
      function l() {
          try {
              y = c(t, b, k)
          } catch(e) {
              h = e,
              y = l
          }
      }
      for (var h, y, d, g, v = [], x = 0;;) switch (g = t.charCodeAt(b++) - 32) {
      case 1:
          u(!v[--x]);
          break;
      case 4:
          v[x++] = f();
          break;
      case 5:
          u(function(e) {
              var a = 0,
              r = e.length;
              return function() {
                  var c = a < r;
                  return c && u(e[a++]),
                  c
              }
          } (v[--x]));
          break;
      case 6:
          y = v[--x],
          u(v[--x](y));
          break;
      case 8:
          if (g = t.charCodeAt(b++) - 32, l(), b += g, g = t.charCodeAt(b++) - 32, y === c) b += g;
          else if (y !== l) return y;
          break;
      case 9:
          v[x++] = c;
          break;
      case 10:
          u(s(v[--x]));
          break;
      case 11:
          y = v[--x],
          u(v[--x] + y);
          break;
      case 12:
          for (y = f(), d = [], g = 0; g < y.length; g++) d[g] = y.charCodeAt(g) ^ g + y.length;
          u(String.fromCharCode.apply(null, d));
          break;
      case 13:
          y = v[--x],
          h = delete v[--x][y];
          break;
      case 14:
          v[x++] = t.charCodeAt(b++) - 32;
          break;
      case 59:
          u((g = t.charCodeAt(b++) - 32) ? (y = x, v.slice(x -= g, y)) : []);
          break;
      case 61:
          u(v[--x][t.charCodeAt(b++) - 32]);
          break;
      case 62:
          g = v[--x],
          k[0] = 65599 * k[0] + k[1].charCodeAt(g) >>> 0;
          break;
      case 65:
          h = v[--x],
          y = v[--x],
          v[--x][y] = h;
          break;
      case 66:
          u(e(t[b++], v[--x], v[--x]));
          break;
      case 67:
          y = v[--x],
          d = v[--x],
          u((g = v[--x]).x === c ? r(g.y, y, k) : g.apply(d, y));
          break;
      case 68:
          u(e((g = t[b++]) < "<" ? (b--, f()) : g + g, v[--x], v[--x]));
          break;
      case 70:
          u(!1);
          break;
      case 71:
          v[x++] = n;
          break;
      case 72:
          v[x++] = +f();
          break;
      case 73:
          u(parseInt(f(), 36));
          break;
      case 75:
          if (v[--x]) {
              b++;
              break
          }
      case 74:
          g = t.charCodeAt(b++) - 32 << 16 >> 16,
          b += g;
          break;
      case 76:
          u(k[t.charCodeAt(b++) - 32]);
          break;
      case 77:
          y = v[--x],
          u(v[--x][y]);
          break;
      case 78:
          g = t.charCodeAt(b++) - 32,
          u(a(v, x -= g + 1, g));
          break;
      case 79:
          g = t.charCodeAt(b++) - 32,
          u(k["$" + g]);
          break;
      case 81:
          h = v[--x],
          v[--x][f()] = h;
          break;
      case 82:
          u(v[--x][f()]);
          break;
      case 83:
          h = v[--x],
          k[t.charCodeAt(b++) - 32] = h;
          break;
      case 84:
          v[x++] = !0;
          break;
      case 85:
          v[x++] = void 0;
          break;
      case 86:
          u(v[x - 1]);
          break;
      case 88:
          h = v[--x],
          y = v[--x],
          v[x++] = h,
          v[x++] = y;
          break;
      case 89:
          u(function() {
              function e() {
                  return r(e.y, arguments, k)
              }
              return e.y = f(),
              e.x = c,
              e
          } ());
          break;
      case 90:
          v[x++] = null;
          break;
      case 91:
          v[x++] = h;
          break;
      case 93:
          h = v[--x];
          break;
      case 0:
          return v[--x];
      default:
          u((g << 16 >> 16) - 16)
      }
  }
  var n = this,
  t = n.Function,
  s = Object.keys ||
  function(e) {
      var a = {},
      r = 0;
      for (var c in e) a[r++] = c;
      return a.length = r,
      a
  },
  b = {},
  k = {};
  global = this;
  global.navigator = {};
  global.navigator.userAgent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"; r(decodeURIComponent("gr%24Daten%20%D0%98b%2Fs!l%20y%CD%92y%C4%B9g%2C(lfi~ah%60%7Bmv%2C-n%7CjqewVxp%7Brvmmx%2C%26eff%7Fkx%5B!cs%22l%22.Pq%25widthl%22%40q%26heightl%22vr*getContextx%24%222d%5B!cs%23l%23%2C*%3B%3F%7Cu.%7Cuc%7Buq%24fontl%23vr(fillTextx%24%24%E9%BE%98%E0%B8%91%E0%B8%A0%EA%B2%BD2%3C%5B%23c%7Dl%232q*shadowBlurl%231q-shadowOffsetXl%23%24%24limeq%2BshadowColorl%23vr%23arcx88802%5B%25c%7Dl%23vr%26strokex%5B%20c%7Dl%22v%2C)%7DeOmyoZB%5Dmx%5B%20cs!0s%24l%24Pb%3Ck7l%20l!r%26lengthb%25%5El%241%2Bs%24j%02l%20%20s%23i%241ek1s%24gr%23tack4)zgr%23tac%24!%20%2B0o!%5B%23cj%3Fo%20%5D!l%24b%25s%22o%20%5D!l%22l%24b*b%5E0d%23%3E%3E%3Es!0s%25yA0s%22l%22l!r%26lengthb%3Ck%2Bl%22%5El%221%2Bs%22j%05l%20%20s%26l%26z0l!%24%20%2B%5B%22cs'(0l%23i'1ps9wxb%26s()%20%26%7Bs)%2Fs(gr%26Stringr%2CfromCharCodes)0s*yWl%20._b%26s%20o!%5D)l%20l%20Jb%3Ck%24.aj%3Bl%20.Tb%3Ck%24.gj%2Fl%20.%5Eb%3Ck%26i%22-4j!%1F%2B%26%20s%2ByPo!%5D%2Bs!l!l%20Hd%3E%26l!l%20Bd%3E%26%2Bl!l%20%3Cd%3E%26%2Bl!l%206d%3E%26%2Bl!l%20%26%2B%20s%2Cy%3Do!o!%5D%2Fq%2213o!l%20q%2210o!%5D%2Cl%202d%3E%26%20s.%7Bs-yMo!o!%5D0q%2213o!%5D*Ld%3Cl%204d%23%3E%3E%3Eb%7Cs!o!l%20q%2210o!%5D%2Cl!%26%20s%2FyIo!o!%5D.q%2213o!%5D%2Co!%5D*Jd%3Cl%206d%23%3E%3E%3Eb%7C%26o!%5D%2Bl%20%26%2B%20s0l-l!%26l-l!i'1z141z4b%2F%40d%3Cl%22b%7C%26%2Bl-l(l!b%5E%26%2Bl-l%26zl'g%2C)gk%7Dejo%7B%7Fcm%2C)%7Cyn~Lij~em%5B%22cl%24b%25%40d%3Cl%26zl'l%20%24%20%2B%5B%22cl%24b%25b%7C%26%2Bl-l%258d%3C%40b%7Cl!b%5E%26%2B%20q%24sign%20"), [TAC = {}]);
  return TAC.sign(behot);
}