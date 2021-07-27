import unittest
import spring_entity_gen


class TestStringMethods(unittest.TestCase):

    def test_class_name_process(self):
        result = {}
        spring_entity_gen.make_java_class_names("Book Author", result)
        self.assertEqual(
            result['java_class_name'],
            "BookAuthor"
        )
        self.assertEqual(
            result['camel_case_plural'],
            "bookAuthors"
        )
        self.assertEqual(
            result['snake_case_plural'],
            "book_authors"
        )
        self.assertEqual(
            result['camel_case'],
            "bookAuthor"
        )
    
    def test_generate_repository_from_template(self):
        content = spring_entity_gen.make_code_from_template(
            {
                'java_class_name': 'BookAuthor',
                'package_name': 'com.package'
            }, 
            spring_entity_gen.REPO_FILE, 
        )
        self.assertEqual(
            content,
            """package com.package.repositories;

import org.springframework.data.repository.PagingAndSortingRepository;


import com.package.models.BookAuthor;

public interface BookAuthorRepository extends PagingAndSortingRepository<BookAuthor, Long> { 

}
"""
        )

    def test_generate_repository_from_entity(self):
        content = spring_entity_gen.make_code_from_template(
            {
                'java_class_name': 'BookAuthor',
                'snake_case_plural': 'book_authors',
                'package_name': 'com.package'
            }, 
            spring_entity_gen.ENTITY_FILE, 
        )
        self.assertEqual(
            content,
            """package com.package.models;

import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;
import lombok.Data;
import javax.persistence.*;


@EqualsAndHashCode(callSuper = true)
@Accessors(chain=true)
@Data
@Entity
@Table(name="book_authors")
public class BookAuthor extends AuditModel {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO, generator = "book_authors_generator")
    @SequenceGenerator(name="book_authors_generator", sequenceName = "book_authors_seq", allocationSize=1)
    @Column(name = "id", updatable = false, nullable = false)
    private long id;
}
"""
        )

    def test_generate_controller_from_template(self):
        self.maxDiff = None
        content = spring_entity_gen.make_code_from_template(
            {
                'java_class_name': 'BookAuthor',
                'camel_case_plural': 'bookAuthors',
                'camel_case': 'bookAuthor',
                'package_name': 'com.package'
            }, 
            spring_entity_gen.CTRL_FILE, 
        )
        self.assertEqual(
            content,
            """package com.package.controllers;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import com.package.models.BookAuthor;
import com.package.repositories.BookAuthorRepository;

@Controller    // This means that this class is a Controller
@RequestMapping(path="/api/v1/bookAuthors")
public class BookAuthorController {

    private final BookAuthorRepository bookAuthorRepository;

    @Autowired
    public BookAuthorController(BookAuthorRepository bookAuthorRepository) {
        this.bookAuthorRepository = bookAuthorRepository;
    }

    @GetMapping(path="/all")
    public @ResponseBody Iterable<BookAuthor> getAllBookAuthor(Pageable page) {
        return bookAuthorRepository.findAll(Pageable.unpaged());
    }
}
"""
        )


if __name__ == "__main__":
    unittest.main()
    