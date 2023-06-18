import React from "react";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import {BrowserRouter as Router, Routes, Route, HashRouter} from 'react-router-dom'
import {Provider} from "react-redux";
import store from "../redux/store";

import { TakePhoto } from "./TakePhoto";



export const App = () => {
 
    return (
        <div >
            <HashRouter>
              <Provider store={store}>
                <Routes>
                  <Route path="/" element={<TakePhoto />} />
                </Routes>
              </Provider>
            </HashRouter>
        </div>
    );
}
