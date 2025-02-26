from sqlalchemy import create_engine, Boolean, Column, ForeignKey, Integer, String, DateTime, Table, DECIMAL, Date, Time
from sqlalchemy.orm import declarative_base, relationship

from .database import Base

persons_addresses = Table('persons_addresses', Base.metadata,
                          Column ('personId', ForeignKey('person.personId'),primary_key=True),
                          Column ('addressId', ForeignKey('address.addressId'),primary_key=True)
                          )

class Person(Base):
    __tablename__= 'person'

    personId = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    priphone = Column(String)
    altphone = Column(String, nullable=True)
    email = Column(String)
    company = Column(String)
    createdat = Column(DateTime)
    addresses= relationship("Address", secondary=persons_addresses, back_populates='persons')
    appointments= relationship("Appointment", back_populates='contact')

class Address(Base):
    __tablename__ = 'address'

    addressId = Column(Integer,primary_key=True,autoincrement=True)
    serviceaddress1 = Column(String)
    serviceaddress2 = Column(String)
    servicecity = Column(String)
    servicestate = Column(String)
    servicezip = Column(Integer)
    servicecounty = Column(String)
    addressType = Column(String)
    persons = relationship("Person", secondary=persons_addresses, back_populates='addresses')

agents_appointments = Table('agents_appointments', Base.metadata,
                          Column ('agent_id', ForeignKey('agents.agent_id'),primary_key=True),
                          Column ('appointment_id', ForeignKey('appointment.appointmentId'),primary_key=True)
                          )

class Appointment(Base):
    __tablename__= 'appointment'

    appointmentId = Column(Integer, primary_key=True, autoincrement=True)
    contactId = Column(Integer, ForeignKey("person.personId"))
    service_id = Column(Integer, ForeignKey("services.id"))
    start_date = Column(DateTime)
    duration = Column(String)
    actualStart = Column(DateTime)
    actualEnd = Column(DateTime)
    flashMessage = Column(String)
    enRouteDisplay = Column(String)
    status = Column(String)
    notes = relationship("AppointmentNotes",back_populates='appointment')
    agents= relationship("Agent", secondary=agents_appointments, back_populates='appointments')
    contact= relationship("Person", back_populates='appointments')
    service= relationship("Services", back_populates='appointment')

class AppointmentNotes(Base):
    __tablename__ = 'appointment_notes'

    note_id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_id = Column(Integer, ForeignKey("appointment.appointmentId"))
    note = Column(String)
    appointment = relationship("Appointment",back_populates='notes')

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    name = Column(String)
    active = Column(Boolean)
    email = Column(String)
    role = Column(String)
    invoiceApprovalsTo = Column(String)
    seePricing = Column(Boolean)
    loggedin = Column(Boolean)
    lastLogin = Column(DateTime)
    created = Column(DateTime)
    updated = Column(DateTime)
    agent = relationship("Agent", back_populates="user")
    timeclock = relationship("UserTime", back_populates="user")

class Agent(Base):
    __tablename__ = "agents"

    agent_id = Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    phone = Column(String)
    sort = Column(Integer)
    internal = Column(Boolean)
    emailNotifications = Column(Boolean)
    startDate = Column(Date)
    endDate = Column(Date)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    user = relationship("User", back_populates="agent")
    appointments = relationship("Appointment", secondary=agents_appointments, back_populates='agents')

class UserTime(Base):
    __tablename__ = "user_time_keeping"

    clock_id = Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    clock_date = Column(Date)
    time_in = Column(DateTime)
    time_out = Column(DateTime)
    total_hours = Column(DECIMAL(4,1))
    user = relationship("User", back_populates="timeclock")

class Parts(Base):
    __tablename__ = "parts"

    id = Column(Integer,primary_key=True)
    category = Column(String)
    name = Column(String)
    description = Column(String)
    unitPrice = Column(DECIMAL(7,2))
    unitCost = Column(DECIMAL(7,2))
    taxable = Column(Boolean)
    active = Column(Boolean)
    created = Column(Date)

class Services(Base):
    __tablename__ = "services"

    id = Column(Integer,primary_key=True)
    name = Column(String)
    category = Column(String)
    description = Column(String)
    unitPrice = Column(DECIMAL(7,2))
    basePrice = Column(DECIMAL(7,2))
    taxable = Column(Boolean)
    active = Column(Boolean)
    created = Column(DateTime)
    updated = Column(DateTime)
    finish = Column(String)
    role = Column(String)
    appointment = relationship("Appointment",back_populates='service')

