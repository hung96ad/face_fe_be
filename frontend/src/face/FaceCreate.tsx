import React, { FC } from 'react';
import {
  Create,
  SimpleForm,
  TextInput,
  SelectInput,
  ReferenceInput
} from 'react-admin';

export const FaceCreate: FC = (props: any) => (
  <Create {...props} title={"Tạo mới nhóm phòng"}>
    <SimpleForm defaultValues={{
      status: true,
    }}>
      <TextInput source="name" required/>
      <TextInput source="path" required/>
      <ReferenceInput source="id_room" label="Phòng" reference="rooms">
        <SelectInput optionText="name" required/>
      </ReferenceInput>
    </SimpleForm>
  </Create>
);
