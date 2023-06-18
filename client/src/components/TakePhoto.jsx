import React, { useEffect, useRef } from "react";
import { useState, useMemo } from "react";
import { useDispatch , useSelector } from "react-redux";

import Camera, { FACING_MODES, IMAGE_TYPES } from "react-html5-camera-photo";

import axios from "axios";  

import 'react-html5-camera-photo/build/css/index.css';
import { uuid } from "../util/Utils";
import { BACKEND_HOST } from "../util/constants";

import '../../assets/style.css';


export const TakePhoto = () => {
    const dispatch = useDispatch();
    const [error, setError] = useState(null);
    const [imageUrl, setImageURL] = useState(null);
    const [image, setImage] = useState(null);
    const [like, setLike] = useState(false);
    const [end, setEnd] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const root = document.querySelector('#root')
        if (loading) {
            root.classList.add('root-opaque');
        } else {
            root.classList.remove('root-opaque');
        }
    }, [loading]);

    useEffect(() => {

    }, [imageUrl]);

    
    const removeBackground = (image) => {
        const form = new FormData();
        form.append("file", image);
        setLoading(true);
        setLike(false);
        setEnd(true);
      
        const options = {
            method: 'POST',
            url: `${BACKEND_HOST}/pic/yup`,
            headers: {
                'Content-Type': 'multipart/form-data;',
            },
            data: form,
        };

        axios.request(options).then(function (response) {
            const data = response.data;
            if (data.code == "fail") {
                setError(data.message);
            } else {
                const url =  `data:image/png;base64,${response.data}`;
                setImageURL(url);   
                setLoading(false);
            }
        }).catch(function (error) {
            console.error(error);
            setError(error);
        });
    };

    const dataURLtoFile = (dataurl, filename) => {
        const   arr = dataurl.split(','),
                mime = arr[0].match(/:(.*?);/)[1],
                bstr = window.atob(arr[1]);
                
        let n = bstr.length;
        const u8arr = new Uint8Array(n);
        while(n--){
            u8arr[n] = bstr.charCodeAt(n);
        }
        
        return new File([u8arr], filename, {type:mime});
    }

    const handleTakePhotoAnimationDone = (dataUri) => {
        setImageURL(dataUri);
        const _image = dataURLtoFile(dataUri);
        setImage(_image);
    };

    const onAgain = () => {
        setImageURL(null);
        setLike(false);
        setEnd(false);
    }

    return (
        <React.Fragment>
            { error != null &&
                <div className="errorTakePhoto">
                    <h1>{error}</h1>
                </div>
            }

            { loading &&
             <div className="vibrate-1  visible">
                 <h2 className="mytext visible">Inferencia en proceso</h2>
             </div>
            }
            
            
            <div className="foto-area">
                { (imageUrl != null)
                    && <img className="photo-taked" src={imageUrl} />
                }
                { (like) &&
                <>
                    <canvas id="canvas"></canvas>
                    <div className="sender-btn">
                        <input type="text" className="text" placeholder="Instagram tag here" />
                        <button className="cbutton" onClick={() => removeBackground(image)}>
                            <span >Enviar a JASA</span>
                            <span className="material-icons-sharp"> rocket_launch </span>
                        </button>
                    </div>
                </>
                }
                { (imageUrl != null) && (end == false) &&
                <div className="controls-btn">
                    <button className="cbutton-red" onClick={() => onAgain()}>
                        <span >De nuevo</span>
                        <span className="material-icons-sharp"> thumb_down </span>
                    </button>
                    <button className="cbutton" onClick={() => setLike(true)}>
                        <span >Me guta!</span>
                        <span className="material-icons-sharp"> thumb_up </span>
                    </button>
                </div>
                }
                { end  &&
                <div className="controls-btn">
                    <button className="cbutton-red" onClick={() => onAgain()}>
                        <span >Cool</span>
                        <span className="material-icons-sharp"> auto_awesome </span>
                    </button>
                </div>
                }
            </div> 
            { (imageUrl == null) &&
            <Camera 
                onTakePhotoAnimationDone={handleTakePhotoAnimationDone}
                imageType = {IMAGE_TYPES.PNG}
                idealFacingMode = {FACING_MODES.ENVIRONMENT}
                isMaxResolution={true}
                // isFullscreen={true}
            />
            }
        </React.Fragment>
    )
};