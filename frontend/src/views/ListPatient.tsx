import React, {useEffect} from 'react';
import { useDispatch, useSelector } from 'react-redux';
import CardItem from '../components/CardItem';
import patient from '../assets/scss/listPatients.module.scss';
import {fetchPatients} from "../store/patientsSlice";
import { RootState, AppDispatch } from '../store';

function ListPatient() {
  const dispatch: AppDispatch = useDispatch();
  const { patients, loading, error } = useSelector((state: RootState) => state.patients);

  useEffect(() => {
    dispatch(fetchPatients());
  }, [dispatch]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className={patient.page}>
      {patients.map((patient) => (
        <CardItem key={patient.id} mainCss='patient'/>
        ))}
    </div>
  )
}

export default ListPatient