/* Άσκηση 01 — ΥΚ1: 3Δ σκηνή με primitives */

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

/* Οθόνη με τη βάση της, πληκτρολόγιο, ποντίκι και πύργος. */
AFRAME.registerComponent('workstation', {
  init: function () {
    this.el.insertAdjacentHTML('beforeend', `
      <a-cylinder mixin="m-plastic" position="0 0.78 -0.14" radius="0.1" height="0.02"></a-cylinder>
      <a-box mixin="m-plastic" position="0 0.87 -0.14" width="0.05" height="0.19" depth="0.05"></a-box>
      <a-box mixin="m-plastic" position="0 1.08 -0.14" width="0.55" height="0.34" depth="0.03" shadow="cast: true"></a-box>
      <a-plane mixin="m-screen" position="0 1.08 -0.12" width="0.51" height="0.3"></a-plane>
      <a-box mixin="m-plastic" position="0 0.78 0.14" width="0.42" height="0.02" depth="0.14"></a-box>
      <a-sphere mixin="m-plastic" position="0.3 0.79 0.14" radius="0.035" scale="1 0.6 1.4"></a-sphere>
      <a-box mixin="m-plastic" position="-0.26 0.21 -0.16" width="0.18" height="0.42" depth="0.42" shadow="cast: true"></a-box>
    `);
  }
});
