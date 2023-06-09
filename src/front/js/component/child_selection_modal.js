import React, { useState, useEffect, useContext } from "react";
import { Modal, Button, Form } from "react-bootstrap";
import { Context } from "../store/appContext";
import { parse, format } from 'date-fns';
import { es } from 'date-fns/locale';
import { useNavigate } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "../../styles/modals.css";
import "../../styles/index.css";
import '../../styles/toastify-custom.css';

export const Child_Selection_Modal = ({ show, onHide, childList }) => {
  const { store, actions } = useContext(Context);

  useEffect(() => {
    console.log("store.tutorData.children:", store.tutorData.children);
  }, [store.tutorData.children]);

  useEffect(() => {
    console.log("esta es la info almacenada en store.selectedChildren: ", store.selectedChildren);
  }, [store.selectedChildren]);

  useEffect(() => {
    if (store.tutorData.children && store.tutorData.children.length > 0) {
      actions.setSelectedChildren(store.tutorData.children);
    }
  }, [store.tutorData.children]);
  
  const handleChildCheckboxChange = (child, checked) => {
    if (checked) {
      actions.setSelectedChildren([...store.selectedChildren, child]);
    } else {
      actions.setSelectedChildren(store.selectedChildren.filter(c => c.id !== child.id));
    }
    console.log("esta es la info almacenada en store.selectedChildren: ", store.selectedChildren)
  };

  const formatDate = (dateString) => {
    const date = parse(dateString, "EEE, dd LLL yyyy HH:mm:ss 'GMT'", new Date());
    const formattedDate = format(date, "EEEE d 'de' MMMM 'del' yyyy 'a las' HH:mm 'horas'", { locale: es });
    return formattedDate;
  };

  const navigate = useNavigate();

  const handleSuccess = (childName) => {
    toast.success(`${childName} ha sido inscripto correctamente!`, {
      onClose: () => {
        navigate("/");
      },
    });
  };
  

  return (
    <Modal show={show} onHide={onHide} centered >
      <Modal.Header closeButton className="custom-modal-header" style={{ backgroundColor: "#feb823" }}>
        <Modal.Title>¿Quiénes se divertirán?</Modal.Title>
      </Modal.Header>
      <Modal.Body  style={{ backgroundColor: "#feb823" }}>
      <p>Seleccione quiénes asistirán el día {formatDate(store.selectedEvent.date)}:</p> 
      <Form>
  {childList && childList.map(child => (
    <Form.Check key={child.id} id={`child-${child.id}`} label={`${child.name} ${child.lastname}`} defaultChecked onChange={e => handleChildCheckboxChange(child, e.target.checked)}/>))}</Form>
      </Modal.Body>
      <Modal.Footer  style={{ backgroundColor: "#feb823" }}>
        <Button variant="secondary" type="button" onClick={onHide}>Cancelar</Button>
        <Button variant="primary" type="button" onClick={() => { actions.handleChildSelectionSubmit(onHide, store.selectedChildren, () => {store.selectedChildren.forEach((child) => { handleSuccess(`${child.name} ${child.lastname}`);});
    });
  }}
>
  Inscribir niños seleccionados
</Button>

        
      </Modal.Footer>
      <ToastContainer />
    </Modal>
  );
};
