'use client'
import {useEffect, useState} from "react";
import {Table,Button,Form,Input,Modal} from "antd";
import axios from "axios";
import { get, post } from "@/utils/requests";

import { message } from 'antd';




export default function AccountsPool() {
    const [dataSource, setDataSource] = useState([])
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [form] = Form.useForm();
    const [verCode,setVerCode] = useState([])
    const [codeHash,setCodeHash] = useState([])
    const handleOk = async () => {
        try {
            // const values = await form.validateFields();
            // console.log('Received values:', values);
            const values = await form.validateFields();
            values.phone_code_hash = codeHash
            console.log(values)
            if (!values.pass_word) {
                values.pass_word = ''
            }
            
            
            // 发送添加账号的请求
            await post('http://127.0.0.1:8000/account/sign-in', values);
        
            setIsModalVisible(false);
            form.resetFields();
            // 刷新列表
            get('http://127.0.0.1:8000/account/get-account-pool')
            .then((res) => {
                console.log(res.data);
                setDataSource(res.data.account_pool); // 确保使用正确的路径
            })
            .catch((err) => {
                console.error('Fetch error:', err);
            });

            // 请求成功后可以刷新列表或显示成功提示
            // setIsModalVisible(false);


        } catch (error) {
            console.error('Validation failed:', error);
        }
    };
    const handleSendCode = async () => {
        const values = await form.validateFields();
        const res = await post('http://127.0.0.1:8000/account/send-code', values)
        if (res.data.phone_code_hash) {
            setCodeHash(res.data.phone_code_hash)
            message.success('发送验证码成功')
        } else {
            message.error('发送验证码失败')
        }


    }

    useEffect(() => {
        document.title = '账号池';
        get('http://127.0.0.1:8000/account/get-account-pool')
            .then((res) => {
                console.log(res.data);
                setDataSource(res.data.account_pool); // 确保使用正确的路径
            })
            .catch((err) => {
                console.error('Fetch error:', err);
            });
    }, []);
    const showModal = () => {
        setIsModalVisible(true);
    };
    const handleCancel = () => {
        setIsModalVisible(false);
    };

    const columns = [
        {
            title: "id"
        },
        {
            title: "手机号",
            dataIndex: "phone_number",
            key: "phone_number"
        },
        {
            title: "用户名",
            dataIndex: "username",
            key: "username"
        },
        {
            title: "账号状态",
            dataIndex: "connected",
            key: "connected",
            render: (text, record) => (
                record.connected ? '已连接' : '未连接'
            )

        }
    ]
    return (
        // 添加账号按钮
        <div>
             <div className="flex justify-end ">
                <Button onClick={showModal}>添加账号</Button>
            </div>

            <h2>账号池</h2>
            <Table dataSource={dataSource} columns={columns} rowKey="phone_number"/>

            <Modal title="添加账号" visible={isModalVisible} onOk={handleOk} onCancel={handleCancel}>
                <Form form={form} layout="vertical">
                    <Form.Item
                        name="phone_number"
                        label="手机号"
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        name="pass_word"
                        label="密码"
                    >
                        <Input.Password />
                    </Form.Item>
                    <Form.Item
                        name="code"
                        label="验证码"
                    >
                        <div style={{ display: 'flex' }}>
                            <Input style={{ flex: 1, marginRight: '10px' }} />
                            <Button onClick={handleSendCode}>发送验证码</Button>
                        </div>
                    </Form.Item>
                </Form>
            </Modal>

        </div>
    );
}
