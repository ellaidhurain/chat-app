import React, { Component } from "react";

import {
  BrowserRouter as Router,
  // Switch,
  Route,
  Link,
  Redirect,
} from "react-router-dom";

export default class HomePage extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <>
      Home page
      </>
      // <Router>
      //   <Switch>
      //     <Route exact path="/">
      //       <p>This is the home page</p>
      //     </Route>
         
      //   </Switch>
      // </Router>
    );
  }
}