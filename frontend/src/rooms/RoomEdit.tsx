import React, { FC } from 'react';
import {
  Edit,
  SimpleForm,
  TextInput,
  SelectInput,
  ReferenceInput,
  AutocompleteInput
} from 'react-admin';
import { Rooms } from '../types';

export const RoomEdit = () => (
  <Edit>
    <SimpleForm>
      <TextInput disabled source="id" />
      <TextInput source="name" />
      <ReferenceInput source="parent_id" label="Nhóm cha" reference="rooms">
        <AutocompleteInput
          optionText={(choice?: Rooms) =>
            choice?.id 
              ? `${choice.name}`
              : ''
          }
        />
      </ReferenceInput>
      <SelectInput source="type_room" disabled choices={[
        { id: 0, name: 'Cơ sở' },
        { id: 1, name: 'Tòa nhà' },
        { id: 2, name: 'Khu vực' },
        { id: 3, name: 'Tầng' },
        { id: 4, name: 'Phòng' },
      ]} />
    </SimpleForm>
  </Edit>
);