import React, {useEffect} from 'react';
import { useDispatch, useSelector } from 'react-redux';
import CardItem from '../components/CardItem';
import patient from '../assets/scss/listPatients.module.scss';
import {fetchPatients} from "../store/patientsSlice";
import { RootState, AppDispatch } from '../store';
import { Button } from '@mantine/core';
import {Navigate, useNavigate} from "react-router-dom";

function ListPatient() {
  const dispatch: AppDispatch = useDispatch();
  const navigate = useNavigate();

  const { patients, loading, error } = useSelector((state: RootState) => state.patients);

  useEffect(() => {
    dispatch(fetchPatients());
  }, [dispatch]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  function handleLogout() {
    localStorage.removeItem('loginTime');
    navigate('/')
  }

  return (
    <div className={patient.page}>
      <div>
        <Button variant="filled" onClick={handleLogout}>Выход</Button>
      </div>
      <div className={patient.listBlock}>
        {patients.map((patient) => (
        <CardItem key={patient.id} mainCss='patient' data={patient}/>
        ))}
      </div>
    </div>
  )
}

export default ListPatient