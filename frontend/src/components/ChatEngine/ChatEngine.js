import React, { useRef, useEffect, useState } from "react";
import Avatar from "./Avatar";
import ChatWindow from "./ChatWindow/ChatWindow";

const ChatEngine = () => {
  const ref = useRef(null); 
  // ref returns a object, current is default property, null is initial value. we can set any value as initial
  // ref = {current:null}

  // after using ref in div element, value of current is set to div
  // ref = {current:div}
 
  const [visible, setVisible] = useState(false);

  const clicked = () => {
    setVisible(!visible);
  };

  // The useEffect Hook allows you to perform side effects in your components. Some examples of side effects are: fetching data, directly updating the DOM
  // useEffect works after component render
  // useEffect triggers functions whenever certain events occur in components
  useEffect(() => {
    // console.log(ref.current);
    function handleClickoutside(e) {
      // current property internally attached by react. to access the value we need to use .current
      // ref.current is returns actual value of ref element 

      //The contains() method is a built-in DOM method that returns a boolean value.
      //e.target element is being passed in as an argument to check the boolean value.
      //where the goal is to determine whether a click event occurred inside a specific DOM element (i.e., the one referenced by ref.current).
      if (!ref.current.contains(e.target)) {
        setVisible(false);
      }
    }
    // document is a global object that represents the current web page loaded in browser.
    document.addEventListener("mousedown", handleClickoutside);
    return () => {
      // cleanup function used for control memory leak
      document.removeEventListener("mousedown", handleClickoutside);
    };

    //whenever the ref variable changed useEffect triggers the function
  }, [ref]);


  return (
    // to access the DOM element in react we need to use ref attribute
    <div ref={ref}>
      <ChatWindow visible={visible} />

      <Avatar
        onClick={clicked}
        style={{ position: "fixed", bottom: "24px", right: "24px" }}
      />
    </div>
  );
};

export default ChatEngine;
