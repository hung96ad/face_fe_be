import React, { FC } from 'react';
import {
  Create,
  SimpleForm,
  TextInput,
  ReferenceInput,
  AutocompleteInput,
} from 'react-admin';
import { Rooms } from '../types';


export const RoomCreate = () => (
  <Create title={"Tạo mới nhóm phòng"}>
    <SimpleForm>
      <TextInput source="name" />
      <ReferenceInput source="parent_id" label="Nhóm cha" reference="rooms">
        <AutocompleteInput
          optionText={(choice?: Rooms) =>
            choice?.id
              ? `${choice.name}`
              : ''
          }
          // defaultValue={null}
          // emptyValue={null}
        />
      </ReferenceInput>
    </SimpleForm>
  </Create>
);
