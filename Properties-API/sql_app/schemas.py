from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field
#from fastapi_filter import FilterDepends

class ReturnBase(BaseModel):
    status: int
    detail: str

class PersonBase(BaseModel):
    personId: Optional[int] = Field(default=None)

class Person(PersonBase):
    name: str
    priphone: str | None
    altphone: str | None
    email: str | None
    company: str | None
    createdat: datetime | None

    class Config:
        orm_mode = True

class AddressBase(BaseModel):
    addressId: Optional[int] = Field(default=None)

class Address(AddressBase):
    serviceaddress1: str | None = None
    serviceaddress2: str | None = None
    servicecity: str | None = None
    servicestate: str | None = None
    servicezip: int | None = None
    servicecounty: str | None = None
    addressType: str | None = None

    class Config:
        orm_mode = True

class Contacts(Person):
    addresses: List[Address]

class AddressSchema(Address):
    contacts: List[Person]


class AgentsBase(BaseModel):
    agent_id: Optional[int] = Field(default=None)

class Agent(AgentsBase):
    #user_id: int | None = None
    phone: str | None = None
    #sort: int | None = None
    internal: bool | None = None
    emailNotifications: bool | None = None
    startDate: date | None = None
    endDate: date | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip: str | None = None

    class Config:
        orm_mode = True

#services
class ServiceBase(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str

class ServiceGet(ServiceBase):
    pass

    class Config:
        orm_mode = True

class ServicePost(BaseModel):
    name: str
    category: str
    description: str
    basePrice: float | None = None
    unitPrice: float | None = None
    taxable: bool | None = None
    active: bool | None = None
    created: datetime | None = None
    updated: datetime | None = None
    finish: str | None = None
    role: str | None = None

    class Config:
        orm_mode = True

class ServicePut(ServiceBase):
    service: ServicePost

    class Config:
        orm_mode = True

class ServiceDelete(ServiceBase):
    pass

    class Config:
        orm_mode = True

class AppointmentNotesBase(BaseModel):
    note_id: Optional[int] = Field(default=None)
    note: str | None = None

    class Config:
        orm_mode = True

class AppointmentsBase(BaseModel):
    appointmentId: Optional[int] = Field(default=None)
    start_date: datetime | None = None
    duration: str | None = None
    status: str | None = None

class AppointmentsGet(AppointmentsBase):
    contact: Contacts
    service: ServiceGet
    actualStart: datetime | None = None
    actualEnd: datetime | None = None
    flashMessage: str | None = None
    enRouteDisplay: str | None = None
    notes: List[AppointmentNotesBase]
    agents: List[AgentsBase]
    
    class Config:
        orm_mode = True

class AppointmentsPost(AppointmentsBase):
    contactId: int | None = None
    service_id: int | None = None
    flashMessage: str | None = None
    enRouteDisplay: str | None = None
    notes: AppointmentNotesBase

    class Config:
        orm_mode = True

class Agents(Agent):
    appointments: List[AppointmentsGet]

class AppointmentsPut(AppointmentsBase):
    service_id: int | None = None
    flashMessage: str | None = None
    enRouteDisplay: str | None = None
    notes: AppointmentNotesBase

    class Config:
        orm_mode = True

#class AppointmentSchema(AppointmentsGet):
#   notes: List[AppointmentNotesBase]
#   agents: List[AgentsBase]

#class AppointmentNotes(Appointments):
#    notes: AppointmentNotesBase


class UserTimeBase(BaseModel):
    clock_id: Optional[int] = Field(default=None)
    user_id: int | None = None
    clock_date: date | None = None

class UserTimeIn(UserTimeBase):
    time_in: datetime | None = None

class UserClockOut(UserTimeBase):
    time_out: datetime | None = None

class UserTimeOut(UserTimeBase):
    time_in: datetime | None = None
    time_out: datetime | None = None
    total_hours: Decimal | None = None

    class Config:
        orm_mode = True

class UsersBase(BaseModel):
    id: Optional[int] = Field(default=None)

class Users(UsersBase):
    name: str | None
    active: bool | None
    email: str | None
    role: str | None
    invoiceApprovalsTo: str | None
    lastLogin: datetime | None
    loggedin: bool | None
    seePricing: bool | None
    created: datetime | None
    updated: datetime | None

    class Config:
        orm_mode = True

class ReturnUsers(Users):
    agent: List[Agent]
    timeclock: list[UserTimeOut]

class UserLoginUpdate(UsersBase):
    lastLogin: datetime | None = None
    loggedin: bool | None

    class Config:
        orm_mode = True

class PartsBase(BaseModel):
    id: Optional[int] = Field(default=None)


class Parts(PartsBase):
    category: str | None = None
    name: str | None = None
    description: str | None = None
    unitPrice: Decimal | None = None
    unitCost: Decimal | None = None
    taxable: bool | None = None
    active: bool | None = None
    created: date | None = None

    class Config:
        orm_mode = True
