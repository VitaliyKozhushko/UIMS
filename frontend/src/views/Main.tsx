import React from "react";
import main from '../asserts/scss/main.module.scss';
import logo from '../asserts/img/logo/logo.png';
import Auth from '../components/AuthForm';

function Main() {
  return (
    <div className={main.page}>
      <div className={main.logoBlock}>
        <img src={logo} alt="Logo" className={main.img}/>
        <div className={main.title}>
          <span className={main.short}>ЕИМС</span>
          <span className={main.full}>Единая информационная медицинская система</span>
        </div>
      </div>
      <div className={main.authBlock}>
        <Auth css={main.auth} cssimg={main.authImg}/>
      </div>
    </div>
  );
}

export default Main;