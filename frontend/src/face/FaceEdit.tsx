import React, { FC } from 'react';
import {
  Edit,
  SimpleForm,
  TextInput,
  SelectInput,
  ReferenceInput,
  BooleanInput
} from 'react-admin';

export const FaceEdit: FC = (props: any) => (
  <Edit {...props}>
    <SimpleForm>
      <TextInput source="name" required />
      <ReferenceInput source="id_room" label="Phòng" reference="rooms">
        <SelectInput optionText="name" required />
      </ReferenceInput>
      <BooleanInput source="status"/>
    </SimpleForm>
  </Edit>
);