// BiKom 20 -> woom helmet rim clip, v20: long arms, zip-tie holes @80%, snap-off seam @85%, interlocking J-teeth, in-arm leaf-spring buttons (no wings, sits flat on its side) on the shell radius, tighter curl at the tips.
// Both arms follow the shell (outer on the shell, inner on the foam) up to the vent, then the last
// `over` mm bends on a tighter radius so the tooth turns into the hole from each side.
// Rail plate hangs vertical below the rim from the INNER edge, so the unit sits right under the rim at the ear.
// Frame: X = inward (into helmet), Y = along the rim (front-back), Z = up.

rim_t   = 24;    // rim thickness at the ear (mm)
wall    = 2.5;   // bridge + plate backing thickness
len     = 30;    // clip length along the rim
plate   = 54;    // rail plate height (long axis vertical)
drop    = wall + 1;  // plate top below the rim bottom - must clear the bridge or it fills the rail slot (v15 bug)

hook_o  = 140;   // outside: rim edge -> vent, along the shell (v14: doubled, was 70)
hook_i  = 120;   // inside:  rim edge -> vent, along the foam (v14: doubled, was 60)
shell_r = 130;   // shell curvature radius over the measured length
over    = 5;     // extension past the vent edge, so the tooth lands inside the hole
tip_r   = 65;    // radius of that extension (twice the bend of the main arm)
hook_d  = 13;    // tooth radial length - each crosses past the shell midline so the two overlap
hook_b  = 3;     // J-hook depth (tangential): outer curls down, inner curls up, they latch
hook_off= 3;     // teeth sit this far above/below the vent line so the J's clear each other
// in-arm leaf springs (horizontal cantilever + button, per the snap-fit video @5:56): a U-slot cut
// through each arm near the base leaves a tongue rooted at the bottom; a round button on its helmet
// side stands proud of the arm, so it is pushed back and preloads against the rim when clipped on
tab_z0  = 6;     // tongue root height above the bridge
tab_l   = 22;    // tongue length
tab_w   = 12;    // tongue width (of len)
slot    = 1;     // slot width around the tongue
btn_r   = 1.6;   // button radius
btn_out = 1.2;   // how far the button stands proud of the arm's helmet-side skin
// plan B: zip ties instead of the interlocking tips
zip_at  = 0.80;  // holes at this fraction of each arm's length
zip_d   = 4;     // hole diameter
zip_sep = 16;    // centre-to-centre spacing of the two holes (along Y)
seam_at = 0.85;  // snap-off seam at this fraction: V-grooves on both faces
seam_r  = 0.6;   // groove radius per face -> leaves arm_t - 2*seam_r of material
hook_w  = 6;     // tooth width (< vent opening)
arm_t   = 2;     // arm thickness (light spring)
preload = 1;     // arms sit this much closer to the helmet than the true surface -> minor clamp

module rail() { rotate([0,90,0]) import("files/HelmetClip.stl"); }

z_bot = -drop - plate;
n = 24;
r_out = shell_r - preload;            // outer arm, shell-side radius
r_in  = shell_r - rim_t + preload;    // inner arm, foam-side radius (concentric with the outer)
deg = 180 / PI;

// path: arc 1 (radius r1, length L1) from (x0,0) curling toward +X, then arc 2 (radius r2, length L2)
// continuing tangentially. `t` offsets the path away from the helmet (concentric skins).
function path(r1, L1, r2, L2, x0, t) = let(
    A1 = L1 / r1 * deg, A2 = L2 / r2 * deg,
    c1 = [x0 + r1, 0],
    P  = c1 + r1 * [-cos(A1), sin(A1)],
    c2 = P + r2 * [cos(A1), -sin(A1)]
  ) concat(
    [for (i = [0:n]) let(a = A1 * i / n) c1 + (r1 + t) * [-cos(a), sin(a)]],
    [for (i = [1:n]) let(a = A1 + A2 * i / n) c2 + (r2 + t) * [-cos(a), sin(a)]]);
function tip_dir(r1, L1, r2, L2) = let(a = (L1 / r1 + L2 / r2) * deg) [cos(a), -sin(a)];  // into the helmet wall

module arm(r1, L1, r2, L2, x0) {
  a = path(r1, L1, r2, L2, x0, 0); b = path(r1, L1, r2, L2, x0, -arm_t);   // -t = away from the helmet
  polygon(concat(a, [for (i = [len(b)-1:-1:0]) b[i]]));
}
// J-tooth: radial shaft `hook_d` long from p along dir, then a hook `hook_b` along `curl`; rounded ends
module tooth(p, dir, curl) rotate([90,0,0]) linear_extrude(hook_w, center=true) {
  hull() { translate(p) circle(r = arm_t/2, $fn = 16); translate(p + hook_d*dir) circle(r = arm_t/2, $fn = 16); }
  hull() { translate(p + hook_d*dir) circle(r = arm_t/2, $fn = 16); translate(p + hook_d*dir + hook_b*curl) circle(r = arm_t/2, $fn = 16); }
}

po = path(r_out, hook_o, tip_r, over, 0, 0);                              // outer arm, shell-side skin
pi_ = path(r_in, hook_i, tip_r - rim_t, over, rim_t, 0);                  // inner arm, foam-side skin
// inner arm: its foam-side skin is the one toward -X, i.e. offset +arm_t toward the centre -> build it mirrored
// fat version of an arm (t from +1 into the helmet to -arm_t-1 outside) restricted to the U-slot bands
module uslot(r1, L1, x0) intersection() {
  rotate([90,0,0]) linear_extrude(len + 2, center=true)
    { a = path(r1, L1, 1, 0.01, x0, 1); b = path(r1, L1, 1, 0.01, x0, -arm_t - 1);
      polygon(concat(a, [for (i = [len(b)-1:-1:0]) b[i]])); }
  union() {
    for (sy = [-1, 1]) translate([-50, sy*(tab_w/2 + slot/2) - slot/2, tab_z0]) cube([200, slot, tab_l]);
    translate([-50, -tab_w/2 - slot, tab_z0 + tab_l - slot]) cube([200, tab_w + 2*slot, slot]);
  }
}
// button on a tongue: cylinder along Y at arc length s on the arm, offset t into the helmet
// side = +1: button sticks toward +X (outer arm -> shell); side = -1: toward -X (inner arm -> foam)
module button(r1, x0, s, side) { a = s / r1 * deg; p = [x0 + r1, 0] + (r1 + (side > 0 ? -(arm_t + btn_out - btn_r) : btn_out - btn_r) - 0.01) * [-cos(a), sin(a)];
  translate([p[0], 0, p[1]]) rotate([90,0,0]) cylinder(r = btn_r, h = tab_w - 2, center = true, $fn = 24); }

// point on an arm at arc length s, offset t from the t=0 skin (body is t in [-arm_t, 0]); and the arm's angle there
function apt(r1, x0, s, t) = let(a = s / r1 * deg, p = [x0 + r1, 0] + (r1 + t) * [-cos(a), sin(a)]) [p[0], 0, p[1]];
function aang(r1, s) = s / r1 * deg;
module zip_holes(r1, x0, L) { a = aang(r1, zip_at * L);
  for (sy = [-1, 1]) translate(apt(r1, x0, zip_at * L, -arm_t/2) + [0, sy * zip_sep/2, 0])
    rotate([0, 90 + a, 0]) cylinder(d = zip_d, h = 20, center = true, $fn = 24); }   // along the arm normal
module seam(r1, x0, L) for (t = [0, -arm_t]) translate(apt(r1, x0, seam_at * L, t))
    rotate([90, 0, 0]) cylinder(r = seam_r, h = len + 2, center = true, $fn = 16);       // groove along Y on each face

difference() {
union() {
  rotate([90,0,0]) linear_extrude(len, center=true) union() {
    polygon([[-arm_t, 0], [-arm_t, -wall], [rim_t, -wall], [rim_t, z_bot], [rim_t + wall, z_bot], [rim_t + wall, 0]]);
    arm(r_out, hook_o, tip_r, over, 0);                                    // outer arm, x in [-arm_t, 0] at the bridge
    { a = path(r_in, hook_i, tip_r - rim_t, over, rim_t, 0);
      b = path(r_in, hook_i, tip_r - rim_t, over, rim_t, -arm_t);         // toward +X (away from foam)
      polygon(concat(a, [for (i = [len(b)-1:-1:0]) b[i]])); }
  }
  // teeth: outer sits hook_off above the vent line and curls down, inner sits below and curls up ->
  // pressing the arms together makes the J's pass, then they latch and the arm preload keeps them tensioned
  no = tip_dir(r_out, hook_o, tip_r, over);  uo = [-no[1], no[0]];        // uo = tangent "up" along the outer arm
  ni = tip_dir(r_in, hook_i, tip_r - rim_t, over); ui = [-ni[1], ni[0]];
  tooth(po[len(po)-1] - 1.5*uo,  no, -uo);                                  // outer: at the arm tip, in, then down
  tooth(pi_[len(pi_)-1] - (1.5 + 2*hook_off)*ui, -ni,  ui);                 // inner: 2*hook_off lower, out, then up
  translate([rim_t - 3 + 0.5, 0, -drop - plate/2]) rail();
  button(r_out, 0, tab_z0 + tab_l - 4, 1);          // outer tongue button, faces the shell
  button(r_in, rim_t, tab_z0 + tab_l - 4, -1);       // inner tongue button, faces the foam
}
  uslot(r_out, hook_o, 0);
  uslot(r_in, hook_i, rim_t);
  zip_holes(r_out, 0, hook_o);  zip_holes(r_in, rim_t, hook_i);
  seam(r_out, 0, hook_o);       seam(r_in, rim_t, hook_i);
}
