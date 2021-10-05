//
//  ViewController.swift
//  thesis-ios
//
//  Created by Andrija Kuzmanov on 6/27/21.
//

import UIKit

class ViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {

    @IBOutlet weak var usernameInput: UITextField!
    @IBOutlet weak var passwordInput: UITextField!
    @IBOutlet weak var loginButton: UIButton!
    @IBOutlet weak var commentBox: UITextView!
    @IBOutlet weak var postButton: UIButton!
    @IBOutlet weak var seekBar: UISlider!
    @IBOutlet weak var seekBarLabel: UILabel!
    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var usernameLabel: UILabel!
    
    var posts: [String] = []
    
    internal func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return posts.count
    }
    internal func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell2 = UITableViewCell(style: UITableViewCell.CellStyle.default, reuseIdentifier: "MyCell")
        cell2.textLabel?.text = posts[indexPath.row]
        return cell2
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        let tap = UITapGestureRecognizer(target: view, action: #selector(UIView.endEditing))
        view.addGestureRecognizer(tap)
        // Do any additional setup after loading the view.
    }
    
    @IBAction func loginButtonOnClick(_ sender: Any) {
        
        let parameters = ["username" : usernameInput.text, "password": passwordInput.text]
        let url = URL(string: "https://andrija-thesis.herokuapp.com/login")!
        let session = URLSession.shared
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        do{
            request.httpBody = try JSONSerialization.data(withJSONObject: parameters, options: .prettyPrinted)
        } catch let error{
            print(error.localizedDescription)
        }
        
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let task = session.dataTask(with: request as URLRequest, completionHandler:{ data, response, error in
            
            guard error == nil else {
                return
            }

            guard let data = data else {
                return
            }
            
            let message = String(decoding: data, as: UTF8.self)
            
            if message == "OK"{
                DispatchQueue.main.async {
                    let storyboard = UIStoryboard(name: "Main", bundle: nil);
                    let vc = storyboard.instantiateViewController(withIdentifier: "SecondPage");
                    self.present(vc, animated: true, completion: nil);
                }
            }
            else if message == "INCORRECT CREDENTIALS" {
                DispatchQueue.main.async {
                    let alert = UIAlertController(title: "Incorrect credentials",
                                                  message: "You entered incorrect username or password. Do you want to try again?",
                                                  preferredStyle: UIAlertController.Style.alert)
                    
                    // add an action (button)
                     alert.addAction(UIAlertAction(title: "Try again", style: UIAlertAction.Style.default, handler: nil))

                     // show the alert
                     self.present(alert, animated: true, completion: nil)
                    
                }
            }
            
        })
        
        task.resume()
        
    }
    
    @IBAction func onSliderValueChanged(_ sender: UISlider) {
        let sliderValue = Int(round(sender.value * 100)).description + "%"
        seekBarLabel.text = sliderValue
    }
    
    @IBAction func postButtonClick(_ sender: Any) {
        if !commentBox.text.isEmpty {
            posts.append(commentBox.text)
            tableView.reloadData()
        }
    }
    
}

