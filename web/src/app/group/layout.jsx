'use client'
import React from 'react';
import { Layout } from 'antd';
import Sidebar from '@/components/Sidebar';
import 'antd/dist/reset.css'; // or 'antd/dist/antd.less'
const { Header, Content, Footer, Sider } = Layout;

const Group = ({ children }) => {
    return (
        <Content>
            {children}

        </Content>


    );
};

export default Group;