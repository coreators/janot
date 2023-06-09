import React, { forwardRef, useEffect, useImperativeHandle, useRef } from "react";
import * as THREE from "three";

class CustomSinCurve extends THREE.Curve<THREE.Vector> {
  private scale: number;

  constructor(scale = 1) {
    super();
    this.scale = scale;
  }

  getPoint(t: number, optionalTarget = new THREE.Vector3()) {
    const pi2 = Math.PI * 2;
    const tx = Math.sin(pi2 * t);
    const ty = Math.cos(pi2 * 3 * t) / 5;

    let dz = 0;
    const tt = (t % 0.25) / 0.25;
    dz = (t % 0.25) - (2 * (1 - tt) * tt * -0.0185 + tt * tt * 0.25);
    if (Math.floor(t / 0.25) == 0 || Math.floor(t / 0.25) == 2) {
      dz *= -1;
    }

    const tz = Math.sin(pi2 * 2 * (t - dz)) / 5;

    return optionalTarget.set(tx, ty, tz).multiplyScalar(this.scale);
  }
}

function easing(t: number, b: number, c: number, d: number) {
  if ((t /= d / 2) < 1) return (c / 2) * t * t + b;
  return (c / 2) * ((t -= 2) * t * t + 2) + b;
}

const CurveAnimation = forwardRef((props, ref) => {
  const canvassize = 400;

  const wireframe = false;
  const color = 0xffffff;

  const length = 40;
  const rotatevalue = 0.035;
  let acceleration = useRef(0);
  let animatestep = useRef(0);
  let toEndRef = useRef(false);
  let isListenRef = useRef(false);
  let isRunningRef = useRef(false);

  const canvasRef = useRef(null);

  useImperativeHandle(ref, () => ({
    listen: listen,
    run: run,
    finish: finish,
    end: end,
  }));

  useEffect(() => {
    const renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(canvassize, canvassize);
    canvasRef.current?.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    const group = new THREE.Group();
    scene.add(group);

    const camera = new THREE.PerspectiveCamera(65, 1, 1, 10000);

    camera.position.z = 150;

    const material = new THREE.MeshBasicMaterial({
      color: color,
      wireframe: wireframe,
    });

    const path = new CustomSinCurve(length - 1);
    const curveGeometry = new THREE.TubeGeometry(
      path as any,
      100,
      0.8,
      2,
      false
    );
    const curveMesh = new THREE.Mesh(curveGeometry, material);
    group.add(curveMesh);

    const ringcover = new THREE.Mesh(
      new THREE.PlaneGeometry(50, 15, 1),
      new THREE.MeshBasicMaterial({
        color: 0xd1684e,
        opacity: 0,
        transparent: true,
      })
    );
    ringcover.position.x = length + 1;
    ringcover.rotation.y = Math.PI / 2;
    group.add(ringcover);

    const ring = new THREE.Mesh(
      new THREE.RingGeometry(5.8, 6.25, 32),
      new THREE.MeshBasicMaterial({
        color: 0xffffff,
        opacity: 0,
        transparent: true,
      })
    );
    ring.position.x = length + 1.1;
    ring.rotation.y = Math.PI / 2;
    group.add(ring);

    // fake shadow
    (function () {
      for (let i = 0; i < 10; i++) {
        const plain = new THREE.Mesh(
          new THREE.PlaneGeometry(length * 2 + 1, 5.6 * 3, 1),
          new THREE.MeshBasicMaterial({
            color: 0xd1684e,
            transparent: true,
            opacity: 0.13,
          })
        );
        plain.position.z = -2.5 + i * 0.5;
        group.add(plain);
      }
    })();

    const render = () => {
      let progress: number;
      animatestep.current = Math.max(
        0,
        Math.min(
          240,
          toEndRef.current ? animatestep.current + 1 : animatestep.current - 4
        )
      );
      if (isListenRef.current) animatestep.current = 40;
      if (isRunningRef.current) animatestep.current = 60;
      acceleration.current = easing(animatestep.current, 0, 1, 240);

      if (acceleration.current > 0.35) {
        progress = (acceleration.current - 0.35) / 0.65;
        group.rotation.y = (-Math.PI / 2) * progress;
        group.position.z = 50 * progress;
        progress = Math.max(0, (acceleration.current - 0.97) / 0.03);
        curveMesh.material.opacity = 1 - progress;
        ringcover.material.opacity = ring.material.opacity = progress;
        ring.scale.x = ring.scale.y = 0.9 + 0.1 * progress;
      }

      renderer.render(scene, camera);
    };

    const animate = () => {
      requestAnimationFrame(animate);
      curveMesh.rotation.x += rotatevalue + acceleration.current;
      render();
    };
    animate();

    return () => canvasRef.current?.removeChild(renderer.domElement);
  }, []);

  const listen = () => {
    toEndRef.current = true;
    isListenRef.current = true;
    isRunningRef.current = false;
  };

  const run = () => {
    toEndRef.current = true;
    isListenRef.current = false;
    isRunningRef.current = true;
  };

  const finish = () => {
    toEndRef.current = true;
    isListenRef.current = false;
    isRunningRef.current = false;
  };

  const end = () => {
    toEndRef.current = false;
  };

  return <div ref={canvasRef} />;
});
CurveAnimation.displayName = "Curve";

export default CurveAnimation;
