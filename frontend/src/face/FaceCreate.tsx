import React, { FC } from 'react';
import {
  Create,
  SimpleForm,
  TextInput,
  SelectInput,
  ReferenceInput,
  ImageInput,
  ImageField
} from 'react-admin';

export const FaceCreate: FC = (props: any) => (
  <Create {...props} title={"Tạo mới nhóm phòng"}>
    <SimpleForm defaultValues={{
      status: true,
    }}>
      <TextInput source="name" required />
      <ReferenceInput source="id_room" label="Phòng" reference="rooms">
        <SelectInput optionText="name" />
      </ReferenceInput>
      <ImageInput source="file" label="Related pictures" accept="image/*">
        <ImageField source="src" title="title" />
      </ImageInput>
    </SimpleForm>
  </Create>
);
