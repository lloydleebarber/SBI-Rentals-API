import datetime
import sys
from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sql_app import models, schemas, database

from fastapi import FastAPI, Depends, HTTPException,status

#contacts
def get_contacts(db: Session, skip: int,limit: int):
    return db.query(models.Person).options(joinedload(models.Person.addresses))\
    .order_by(models.Person.personId)\
    .offset(skip).limit(limit).all()

def get_contact_by_id(id:int, db: Session):
    return db.query(models.Person).options(joinedload(models.Person.addresses))\
    .filter (models.Person.personId == id).first()

def add_new_address(id:int,address: schemas.Address, db: Session):
    addr_query = db.query(models.Address)\
    .filter((models.Address.serviceaddress1 == address.serviceaddress1)\
    & (models.Address.servicezip == address.servicezip)).one()
    addr_found = addr_query

    addr_id = addr_found.addressId

    if not addr_found:
        #raise HTTPException(status_code=status.HTTP_302_FOUND,
        #                    detail=f'An address with this name: ({address.serviceaddress1}) already exists')
    
        new_address = models.Address(**address.dict(exclude_unset=True))
        db.add(new_address)
        db.commit()
        #db.refresh(new_address) 
        addr_added = db.query(models.Address)\
        .filter((models.Address.serviceaddress1 == address.serviceaddress1)\
        & (models.Address.servicezip == address.servicezip)).one()
        addr_new = addr_added

        addr_id = addr_new.addressId

    connect_addr_to_person(id, addr_id, db)

    return models.Person

def connect_addr_to_person(id,addrId, db):
    
    persons_addresses = insert(models.persons_addresses).values(personId=id,addressId=addrId)
    db.execute(persons_addresses)
    db.commit()
    db.close()
    #db.refresh(persons_addresses)

    return f'Address Added'

#appoointments
def get_appointments(db: Session, agent_id: int | None, skip: int,limit: int):
    if agent_id: 
        _query = db.query(models.Appointment).options(joinedload(models.Appointment.agents))\
        .filter(models.Appointment.agents.any(models.Agent.agent_id.in_([agent_id])))\
        .order_by(models.Appointment.appointmentId)\
        .offset(skip).limit(limit).all()
    else:
         _query = db.query(models.Appointment).options(joinedload(models.Appointment.agents))\
        .order_by(models.Appointment.appointmentId)\
        .offset(skip).limit(limit).all()

    return _query

def get_appointment_by_id(id:int, db: Session):
    return db.query(models.Appointment)\
    .filter (models.Appointment.id == id).first()

def add_new_appointment(appointment: schemas.AppointmentsPost,agents: List[schemas.AgentsBase], db: Session):
    _query = db.query(models.Appointment)\
    .filter((models.Appointment.contactId == appointment.contactId)\
    & (models.Appointment.start_date == appointment.start_date)).first()
    _found = _query

    #_id = _found.contactId

    if not _found:
        #raise HTTPException(status_code=status.HTTP_302_FOUND,
        #                    detail=f'An address with this name: ({address.serviceaddress1}) already exists')
       
    
        new_appt = models.Appointment(**appointment.dict(exclude_unset=True))
        db.add(new_appt)
        db.commit()
        db.refresh(new_appt) 
        _added = db.query(models.Appointment)\
        .filter((models.Appointment.contactId == appointment.contactId)\
            & (models.Appointment.start_date == appointment.start_date)).one()
        _new = _added

        appt_id = _new.appointmentId
        for agent in agents:
            connect_agents_to_appt(appt_id, agent.agent_id, db)

    return {"status": status.HTTP_200_OK, "detail": "Appointment created"}

def connect_agents_to_appt(id, agent, db):
    _insert_bridge = insert(models.agents_appointments).values(appointment_id=id,agent_id=agent)
    db.execute(_insert_bridge)
    db.commit()

    return f'Address Added'

def update_appointment(id:int,appointment: schemas.AppointmentsPut, db: Session):
    _query = db.query(models.Appointment).filter(models.Appointment.id == id)
    _found = _query.first()

    if not _found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Appointment not found')
    
    update_data = appointment.dict(exclude_unset=True)
    part_query.filter(models.Appointment.id == id).update(update_data, # type: ignore
                                                       synchronize_session=False)
    
    db.commit()
    db.refresh(_found)
    
    return get_appointment_by_id(id,db)

#users
def get_users(db: Session, skip: int,limit: int):
    return db.query(models.User)\
    .order_by(models.User.id)\
    .offset(skip).limit(limit).all()

def get_user_by_id(id:int, db: Session):
    return db.query(models.User)\
    .filter (models.User.id == id).first()

def get_user_login(email, db: Session):
    user = db.query(models.User)\
    .filter (models.User.email == email).first()

    user_found = user

    if not user_found:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'A user with this email: ({email}) does not exist')
    
    user_email = user_found.email

    return user

def update_user_login(id:int,user: schemas.UserLoginUpdate, db: Session):
    _query = db.query(models.User).filter(models.User.id == id)
    _found = _query.first()

    if not _found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User not found in database')
    
    update_data = user.model_dump(exclude_unset=True)
    _query.filter(models.User.id == id).update(update_data, # type: ignore
                                                       synchronize_session=False)
    
    db.commit()
    db.refresh(_found)
    
    return {"status": status.HTTP_200_OK, "detail": "User log data updated."}

#parts
def get_parts(db: Session, skip: int,limit: int):
    return db.query(models.Parts)\
    .order_by(models.Parts.id)\
    .offset(skip).limit(limit).all()

def get_part_by_id(id: int, db: Session):
    return db.query(models.Parts)\
    .filter (models.Parts.id == id).first()

def update_part_by_id(id:int,part: schemas.Parts, db: Session):
    part_query = db.query(models.Parts).filter(models.Parts.id == id)
    part_found = part_query.first()

    if not part_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No part with this id: {id} found')
    
    update_data = part.dict(exclude_unset=True)
    part_query.filter(models.Parts.id == id).update(update_data, # type: ignore
                                                       synchronize_session=False)
    
    db.commit()
    db.refresh(part_found)
    
    return get_part_by_id(id,db)

def create_part(part: schemas.Parts, db: Session):
    part_query = db.query(models.Parts).filter(models.Parts.name == part.name)
    part_found = part_query.first()

    if part_found:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail=f'A part with this name: ({part.name}) already exists')
    
    new_part = models.Parts(**part.dict())
    db.add(new_part)
    
    db.commit()
    db.refresh(new_part)
    
    return schemas.Parts

def delete_part_by_id(id:int, db: Session):
    part_query = db.query(models.Parts).filter(models.Parts.id == id)
    part_found = part_query.first()

    if not part_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No part with this id: {id} exists')
    
    part_query.delete(synchronize_session=False)
    
    db.commit()
    
    return {"status": status.HTTP_200_OK, "detail": "Record deleted permanently from database."}

def create_time_entry(clock: schemas.UserTimeIn, db: Session):

    time_query = db.query(models.Agent).filter(models.Agent.user_id == clock.user_id).first()
    entry_found = time_query

    #user_id = entry_found.user_id

    if not entry_found:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'User could not be found or user id not provided')
    
    new_entry = models.UserTime(**clock.dict())
    db.add(new_entry)
    
    db.commit()
    db.refresh(new_entry)
    
    return {"status": status.HTTP_200_OK, "detail": "Time entered successfully"}

def out_time_entry(clock: schemas.UserClockOut, db: Session):

    query = db.query(models.UserTime).filter((models.UserTime.user_id == clock.user_id)\
        & (models.UserTime.time_out == None))
    _found = query.first()

    if not _found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User is not clocked in')
    
    update_data = clock.dict(exclude_unset=True)
    query.filter((models.UserTime.user_id == clock.user_id)\
                 & (models.UserTime.time_out == None))\
                    .update(update_data, # type: ignore
                                                       synchronize_session=False)
    
    db.commit()
    db.refresh(_found)
    
    return {"status": status.HTTP_200_OK, "detail": "Time updated successfully"}

def admin_time_modify(clock_id: int, clock: schemas.UserTimeOut, db: Session):

    query = db.query(models.UserTime).filter(models.UserTime.clock_id == clock_id)
    _found = query.first()

    if not _found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Time entry could not be modified')
    
    update_data = clock.dict(exclude_unset=True)
    query.filter(models.UserTime.clock_id == clock_id)\
                    .update(update_data, # type: ignore
                                                       synchronize_session=False)
    
    db.commit()
    db.refresh(_found)
    
    return {"status": status.HTTP_200_OK, "detail": "Time updated successfully"}

def delete_time_entry(clock_id:int, db: Session):
    query = db.query(models.UserTime).filter(models.UserTime.clock_id == clock_id)
    _found = query.first()

    if not _found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No time entry with this id: {clock_id} exists')
    
    query.delete(synchronize_session=False)
    
    db.commit()
    
    return {"status": status.HTTP_200_OK, "detail": "Record deleted permanently from database."}