var express = require('express');
var { graphqlHTTP } = require('express-graphql');
var { buildSchema } = require('graphql');
 
var schema = buildSchema(`
  type User {
    id: String
    name: String
  }
  
   type Student {
    studentid: String
    studentname: String
    studentdob: String
  }
 

  type Query {
    usercall(id: String): User
    studentQueryById(studentid: String): Student
    studentQueryByName(studentname: String): [Student]
    studentQueryByDob(studentdob: String): [Student]
    othercall: String
  }
`);
 
// Maps id to User object
var fakeDatabase = {
  'a': {
    id: 'a',
    name: 'alice',
  },
  'b': {
    id: 'b',
    name: 'bob',
  },
  'c': {
    id: 'c',
    name: 'carl',
  },
  
};

var studentDatabase = {
 'a': {
    studentid: 'b00001',
    studentname: 'alice',
    studentdob: '99'
  },
  'b': {
    studentid: 'b00002',
    studentname: 'bob',
    studentdob: '88'
  },
  'c': {
    studentid: 'b00003',
    studentname: 'tom',
    studentdob: '91'
  },
  'd': {
    studentid: 'b00004',
    studentname: 'jim',
    studentdob: '94'
  },
  'e': {
    studentid: 'b00005',
    studentname: 'bill',
    studentdob: '99'
  },
    
};
 
var root = {
  usercall: ({id}) => {
    return fakeDatabase[id]; // mapping to the data
  },
  
  studentQueryById: ({studentid}) => {
     // send back the data  
     
    for (let [key, value] of Object.entries(studentDatabase)) {
      if(value.studentid == studentid)
      {
        return studentDatabase[key]
      }
    }
  },
  studentQueryByName: ({studentname}) => {
     // send back the data   
     var output = []; 
     for (let [key, value] of Object.entries(studentDatabase)) {
      if(value.studentname == studentname)
      {
        output.push(studentDatabase[key])
      }
    }
    return output
  },
  studentQueryByDob: ({studentdob}) => {
     // send back the data 
     var output = []; 
     for (let [key, value] of Object.entries(studentDatabase)) {
      if(value.studentdob == studentdob)
      {
        output.push(studentDatabase[key])
      }
    }
    return output
  },
  
  
   othercall: ({}) => {
  return 'This is the other call';
  }
};
 
var app = express();
app.use('/graphql', graphqlHTTP({
  schema: schema,
  rootValue: root,
  graphiql: true,
}));
app.listen(4000);
console.log('Running a GraphQL API server at localhost:4000/graphql');