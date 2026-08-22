/* Άσκηση 02 — ΥΚ1: υφές και φωτισμός */

/* Η καρέκλα και η θέση εργασίας επαναλαμβάνονται δεκάδες φορές μέσα στην
   αίθουσα. Αντί να γραφτούν τα ίδια primitives κάθε φορά στο index.html,
   μπαίνουν εδώ μία φορά και προστίθενται ως παιδιά της οντότητας. */

AFRAME.registerComponent('chair', {
  init: function () {
    this.el.insertAdjacentHTML('beforeend', `
      <a-box mixin="m-chair" position="0 0.44 0" width="0.44" height="0.07" depth="0.42" shadow="cast: true"></a-box>
      <a-box mixin="m-chair" position="0 0.76 0.21" rotation="-10 0 0" width="0.42" height="0.36" depth="0.06" shadow="cast: true"></a-box>
      <a-cylinder mixin="m-tube" position="-0.19 0.59 0.2" rotation="-10 0 0" radius="0.015" height="0.34"></a-cylinder>
      <a-cylinder mixin="m-tube" position="0.19 0.59 0.2" rotation="-10 0 0" radius="0.015" height="0.34"></a-cylinder>
      <a-cylinder mixin="m-tube" position="-0.19 0.21 -0.18" radius="0.016" height="0.42"></a-cylinder>
      <a-cylinder mixin="m-tube" position="0.19 0.21 -0.18" radius="0.016" height="0.42"></a-cylinder>
      <a-cylinder mixin="m-tube" position="-0.19 0.21 0.18" radius="0.016" height="0.42"></a-cylinder>
      <a-cylinder mixin="m-tube" position="0.19 0.21 0.18" radius="0.016" height="0.42"></a-cylinder>
      <a-box mixin="m-tube" position="-0.19 0.13 0" width="0.02" height="0.02" depth="0.36"></a-box>
      <a-box mixin="m-tube" position="0.19 0.13 0" width="0.02" height="0.02" depth="0.36"></a-box>
      <a-box mixin="m-tube" position="0 0.13 -0.18" width="0.38" height="0.02" depth="0.02"></a-box>
      <a-box mixin="m-tube" position="0 0.13 0.18" width="0.38" height="0.02" depth="0.02"></a-box>
    `);
  }
});

/* Οθόνη (βάση και πλαίσιο), πληκτρολόγιο, ποντίκι και πύργος. Η εικόνα της
   οθόνης γράφεται στο index.html, γιατί αλλάζει από θέση σε θέση. */
AFRAME.registerComponent('workstation', {
  init: function () {
    this.el.insertAdjacentHTML('beforeend', `
      <a-cylinder mixin="m-plastic" position="0 0.78 -0.14" radius="0.1" height="0.02"></a-cylinder>
      <a-box mixin="m-plastic" position="0 0.87 -0.14" width="0.05" height="0.19" depth="0.05"></a-box>
      <a-box mixin="m-plastic" position="0 1.08 -0.14" width="0.55" height="0.34" depth="0.03" shadow="cast: true"></a-box>
      <a-box mixin="m-keyboard" position="0 0.78 0.14" width="0.42" height="0.02" depth="0.14"></a-box>
      <a-sphere mixin="m-plastic" position="0.3 0.79 0.14" radius="0.035" scale="1 0.6 1.4"></a-sphere>
      <a-box mixin="m-plastic" position="-0.26 0.21 -0.16" width="0.18" height="0.42" depth="0.42" shadow="cast: true"></a-box>
      <a-plane mixin="m-pc" position="-0.26 0.21 0.06" width="0.17" height="0.4"></a-plane>
    `);
  }
});

/* Τρεις προρυθμίσεις φωτισμού, με εναλλαγή από το πλήκτρο L ή το κουμπί του HUD. */
AFRAME.registerComponent('lighting-presets', {
  init: function () {
    var presets = [
      { name: 'μέρα',      sun: 0.85, amb: 0.22, hemi: 0.18, lamp: 9,  spot: 28, beam: 0.07, sky: '#ffffff' },
      { name: 'εσπερινός', sun: 0.35, amb: 0.20, hemi: 0.15, lamp: 28, spot: 38, beam: 0.15, sky: '#e8bb92' },
      { name: 'προβολή',   sun: 0.05, amb: 0.06, hemi: 0.04, lamp: 1,  spot: 69, beam: 0.30, sky: '#41527a' }
    ];
    var i = 0;

    function set(selector, component, property, value) {
      document.querySelectorAll(selector).forEach(function (el) {
        el.setAttribute(component, property, value);
      });
    }

    function apply() {
      var p = presets[i];
      set('#sun', 'light', 'intensity', p.sun);
      set('#ambient', 'light', 'intensity', p.amb);
      set('#hemi', 'light', 'intensity', p.hemi);
      set('.lamp', 'light', 'intensity', p.lamp);
      set('#projector-beam', 'light', 'intensity', p.spot);
      set('#beam-cone', 'material', 'opacity', p.beam);
      set('a-sky', 'material', 'color', p.sky);
      document.querySelector('#preset-label').textContent = p.name;
    }

    function next() {
      i = (i + 1) % presets.length;
      apply();
    }

    document.querySelector('#preset-button').addEventListener('click', next);
    window.addEventListener('keydown', function (e) {
      if (e.code === 'KeyL') { next(); }
    });

    apply();
  }
});

/* Οι browsers δεν ξεκινούν βίντεο χωρίς ενέργεια του χρήστη, οπότε η οθόνη
   με το βίντεο ξεκινά με το κλικ. */
window.addEventListener('click', function () {
  document.querySelector('#texVideo').play();
});
