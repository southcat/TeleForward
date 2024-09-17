'use client'
import { useState } from 'react';
import { setToken } from '../utils/token';
import { Input, Button, Form, message } from 'antd';

export default function Home() {
  const [form] = Form.useForm();

  const handleSubmit = (values) => {
    setToken(values.password);
    form.resetFields();
    message.success('Token已保存');
  };

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto', padding: '20px' }}>
      <h2>欢迎来到主页</h2>
      <p>这是主页的主要内容。</p>
      
      <Form form={form} onFinish={handleSubmit}>
        <Form.Item
          name="password"
          label="输入Token"
          rules={[{ required: true, message: '请输入Token' }]}
        >
          <Input.Password placeholder="请输入Token" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit">
            保存Token
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}
