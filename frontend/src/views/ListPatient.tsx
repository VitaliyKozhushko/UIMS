import React from 'react';
import CardItem from '../components/CardItem';
import patient from '../assets/scss/listPatients.module.scss';

function ListPatient() {
  return (
    <div className={patient.page}>
      <CardItem mainCss='patient'/>
    </div>
  )
}

export default ListPatient