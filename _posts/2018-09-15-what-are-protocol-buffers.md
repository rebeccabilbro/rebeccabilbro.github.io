---
layout: post
title:  What are Protocol Buffers?
image:
  feature: pepper_crop.png
date:   2018-09-15 15:50
categories: programming
---

Protocol buffers are a way of serializing data so that it can be efficiently sent between programs. It is structured in a way that is reminiscent of XML or JSON, but designed to produce much more compact (albeit no longer human-readable) messages. In this post we'll explore a bit about the use cases of protobufs, how they work, and what they look like.

## Sending data back and forth

When we serialize data, we translate it into a format that is better for storage or transmittal. For example, when we [pickle](http://scikit-learn.org/stable/modules/model_persistence.html) a fitted scikit-learn pipeline or store a neural network model as an [HDF5](https://support.hdfgroup.org/HDF5/), we're serializing the data structures (matrices, graphs, etc.) of the models along with their hyperparameters, weights, and state. Just as you can load a sklearn model (`pickle.load(open(saved_model.pkl, 'rb'))` or `joblib.load(saved_model.pkl)`) or a Keras model (`load_model('saved_model.h5')`), any serialized data can be used to restore the original objects.

> "This process of serializing an object is also called marshalling an object. The opposite operation, extracting a data structure from a series of bytes, is deserialization (which is also called Unmarshalling)." - ["Serialization," Wikipedia](https://en.wikipedia.org/wiki/Serialization)

[XML](https://en.wikipedia.org/wiki/XML_Schema_(W3C)) (eXtensible Markup Language) is one standard for data serialization. It is good for representing complex, hierarchical data, and it is also human-readable (if not very pretty). Unlike HTML, XML was designed to transmit (not display) data. It's more flexible for data transmission because XML tags aren't predefined; you can come up with your own schema that suits your data, and then you can write programs that systematically serialize your data using that schema, and other programs that translate it back to data on the other end.

[JSON](https://en.wikipedia.org/wiki/JSON) (JavaScript Object Notation) is another way to serialize complex data; objects can be encoded as attribute–value pairs. Like XML, JSON is very flexible and human-readable, but less verbose. It's often a default storage tool of choice for Python programmers because Python `dicts` can be mapped directly to JSON, and vice versa.

One advantage of JSON (and XML) is that when you're consuming it, you don't have to have the schema to parse it; this ends up being enormously helpful for data scientists who interact with public APIs and don't always have a robust contract with the backend providing the data. Since these formats are human-readable, they require a lot less coordination between backend and frontend.

On the other hand, this human-readability comes at a cost; neither XML nor JSON is very compact. And if it's not two humans communicating, that cost might not be worth paying if it means unnecessary throughput and unwanted latency.

## What are protobufs?

Originally developed for internal use at Google, protocol buffers (protobufs) are a way of serializing data so that it can be more efficiently sent between programs. It is structured in a way that is reminiscent of XML or JSON.

However, unlike XML or JSON, this approach serializes message into a dense binary (and thus much more compact) format. Read alone, these serialized messages are not self-describing; you can't read a protobuf and understand what's in the message the way you can with an XML or JSON document.

## Protobufs in Python

*Fair warning, this is assuming you have a Mac.*

1. [Download and untar pre-built binary](https://github.com/protocolbuffers/protobuf/releases)
2. Follow the instructions [here](https://medium.com/@erika_dike/installing-the-protobuf-compiler-on-a-mac-a0d397af46b8). Note: you may need to `brew install libtool` as well as `brew install autoconf && brew install automake`.
3. `pip install protobuf`

## Anatomy of a protobuf message

For [example](https://github.com/protocolbuffers/protobuf/tree/master/examples), let's say we want to pass around messages that contain information for an address book.

First, we need to define the schema for the data in a `.proto` file. This schema will map data types with field names (represented as integers). We begin by formally defining what an acquaintance is in our `Person` message type.

A `Person` will have a name, a unique identifier, and an email. They'll also have several different ways of contacting them (cell, home phone, work phone, or other miscellaneous number), which we'll define as a new message type `PhoneNumber`, each of which will have a contact number associated with it. Finally, since people's phone numbers, emails, and names sometimes change, we'll include a timestamp to remember when we added this contact's information:

```
message Person {
  string name = 1;
  int32 id = 2;  // Unique ID number for this person.
  string email = 3;

  enum PhoneType {
    MOBILE = 0;
    HOME = 1;
    WORK = 2;
  }

  message PhoneNumber {
    string number = 1;
    PhoneType type = 2;
  }

  repeated PhoneNumber phones = 4;

  google.protobuf.Timestamp last_updated = 5;
}

```

Finally, we'll add a message type to our `.proto` that defines an `AddressBook` as simply a collection of `Persons`

```
message AddressBook {
  repeated Person people = 1;
}
```

Next we can write a script for adding entries to our `AddressBook` that leverages what we have defined about how we expect new acquaintances to be entered into our book. The stock example imagines this will be done via the command line:

```python
import sys
import addressbook_pb2


def get_address(person):
    """
    Fills in a "Person" message based on user input.
    """
    person.id = int(input("Enter person ID number: "))
    person.name = input("Enter name: ")

    email = input("Enter email address (blank for none): ")
    if email != "":
        person.email = email

    while True:
        number = input("Enter a phone number (or leave blank to finish): ")
        if number == "":
            break

        phone_number = person.phones.add()
        phone_number.number = number

        type = input("Is this a mobile, home, or work phone? ")
        if type == "mobile":
            phone_number.type = addressbook_pb2.Person.MOBILE
        elif type == "home":
            phone_number.type = addressbook_pb2.Person.HOME
        elif type == "work":
            phone_number.type = addressbook_pb2.Person.WORK
        else:
            print("Unknown phone type; leaving as default value.")


if __name__ == '__main__':
    # Read the entire address book from a file, parses user input
    # to add one person, then writes it back out to the same file.
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "ADDRESS_BOOK_FILE")
        sys.exit(-1)

    address_book = addressbook_pb2.AddressBook()

    # Read the existing address book.
    try:
        with open(sys.argv[1], "rb") as f:
            address_book.ParseFromString(f.read())
    except IOError:
        print(sys.argv[1] + ": File not found.  Creating a new file.")

    # Add an address.
    get_address(address_book.people.add())

    # Write the new address book back to disk.
    with open(sys.argv[1], "wb") as f:
        f.write(address_book.SerializeToString())
```

Now that we know how to enter new acquaintances into our `AddressBook`, we can write a script that reads from protobuf format to produce a human-readable version of the address book:

```python
import sys
import addressbook_pb2


def list_people(address_book):
    """
    Iterate though all people in AddressBook and print their contact details
    """
    for person in address_book.people:
        print("Person ID:", person.id)
        print("  Name:", person.name)

        if person.email != "":
            print("  E-mail address:", person.email)

        for phone_number in person.phones:
            if phone_number.type == addressbook_pb2.Person.MOBILE:
                print("  Mobile phone #:", end=" ")
            elif phone_number.type == addressbook_pb2.Person.HOME:
                print("  Home phone #:", end=" ")
            elif phone_number.type == addressbook_pb2.Person.WORK:
                print("  Work phone #:", end=" ")
            print(phone_number.number)

if __name__ == '__main__':
    # Read entire address book from file and print information
    # in a human-readable form to the command line.
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "ADDRESS_BOOK_FILE")
        sys.exit(-1)

    address_book = addressbook_pb2.AddressBook()

    # Read the existing address book.
    with open(sys.argv[1], "rb") as f:
        address_book.ParseFromString(f.read())

    list_people(address_book)
```

Once compiled, this code becomes an encoding/decoding script that can be used by both the sender and the receiver of the messages. With `make`, the above two Python files build two shell scripts that can be run as executables:

```bash
$ ./add_person_python addressbook.data
$ ./list_people_python addressbook.data
```


## Further Reading/Watching

 - [Protocol Buffers - Developer Docs](https://developers.google.com/protocol-buffers/)
 - [Protocol Buffer Examples in C++, Java, Python, and Go](https://github.com/protocolbuffers/protobuf/tree/master/examples)
 - [An Introduction to Protobufs by Ten Loh](https://youtu.be/72mPlAfHIjs)
 - [justforfunc #30: The Basics of Protocol Buffers](https://youtu.be/_jQ3i_fyqGA)
 - [Installing the Protobuf Compiler on a Mac by Erika Dike](https://medium.com/@erika_dike/installing-the-protobuf-compiler-on-a-mac-a0d397af46b8)
 - [JSON vs XML vs Protobufs on Stackoverflow](https://stackoverflow.com/questions/14028293/google-protocol-buffers-vs-json-vs-xml)
